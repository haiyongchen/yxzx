# -*- coding: utf-8 -*-
"""
处理任务使用表数据，统计总人工成本和上线前人工成本
"""

import pandas as pd
from pathlib import Path
import numpy as np

def process_task_cost():
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    stats_file = base_dir / "专区接入情况统计表.xlsx"
    task_file = base_dir / "任务使用表.xls"
    
    print("=" * 60)
    print("开始处理任务使用表数据")
    print("=" * 60)
    
    # 读取统计表
    print(f"\n1. 读取统计表...")
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    print(f"   统计表行数: {len(df_stats)}")
    
    # 获取合同号列（A列，索引0）和专区上线时间列（索引15）
    contract_col = df_stats.columns[0]  # 合同号
    online_time_col = df_stats.columns[15]  # 专区上线时间
    print(f"   合同号列(A列): {contract_col}")
    print(f"   专区上线时间列: {online_time_col}")
    
    # 读取任务使用表
    print(f"\n2. 读取任务使用表...")
    df_task = pd.read_excel(task_file, sheet_name=0)
    print(f"   任务使用表行数: {len(df_task)}")
    
    # 查看任务使用表的列名
    print(f"\n   任务使用表列名:")
    for i, col in enumerate(df_task.columns):
        print(f"     {i}: {col}")
    
    # 获取需要的列
    # K列：合同编号（索引10）
    # F列：实际开始时间（索引5）
    # I列：实际人工成本（索引8）
    task_contract_col = df_task.columns[10]  # K列：合同编号
    task_start_col = df_task.columns[5]      # F列：实际开始时间
    task_cost_col = df_task.columns[8]       # I列：实际人工成本
    
    print(f"\n   使用的列:")
    print(f"     合同编号列(K列): {task_contract_col}")
    print(f"     实际开始时间列(F列): {task_start_col}")
    print(f"     实际人工成本列(I列): {task_cost_col}")
    
    # 初始化新列
    print("\n3. 初始化新列...")
    df_stats['总人工成本'] = 0.0
    df_stats['上线前人工成本'] = 0.0
    
    # 处理每个合同
    print("\n4. 统计人工成本...")
    
    # 按合同编号分组统计总人工成本
    total_cost_by_contract = df_task.groupby(task_contract_col)[task_cost_col].sum()
    
    # 处理每个统计表中的行
    match_count = 0
    for idx, row in df_stats.iterrows():
        contract_no = str(row[contract_col]).strip()
        online_time = row[online_time_col]
        
        # 处理多个合同号（用分号或中文分号分隔）
        contract_list = [c.strip() for c in contract_no.replace('；', ';').split(';') if c.strip()]
        
        total_cost = 0.0
        pre_online_cost = 0.0
        has_match = False
        
        for single_contract in contract_list:
            # 统计总人工成本
            if single_contract in total_cost_by_contract.index:
                total_cost += total_cost_by_contract[single_contract]
                has_match = True
                
                # 统计上线前人工成本
                if pd.notna(online_time):
                    try:
                        if not isinstance(online_time, pd.Timestamp):
                            online_time = pd.to_datetime(online_time)
                        # 筛选该合同且实际开始时间在上线时间之前的记录
                        task_start_times = pd.to_datetime(df_task[task_start_col], errors='coerce')
                        task_records = df_task[
                            (df_task[task_contract_col] == single_contract) & 
                            (task_start_times <= online_time) &
                            (task_start_times.notna())
                        ]
                        
                        if len(task_records) > 0:
                            pre_online_cost += task_records[task_cost_col].sum()
                    except:
                        pass  # 跳过有问题的数据
        
        # 如果有匹配的数据，更新统计表
        if has_match:
            df_stats.at[idx, '总人工成本'] = total_cost
            df_stats.at[idx, '上线前人工成本'] = pre_online_cost
            match_count += 1
    
    print(f"   匹配成功: {match_count} 条")
    
    # 统计
    print("\n5. 统计结果:")
    has_total_cost = (df_stats['总人工成本'] > 0).sum()
    has_pre_online_cost = (df_stats['上线前人工成本'] > 0).sum()
    print(f"   有总人工成本的平台数: {has_total_cost}")
    print(f"   有上线前人工成本的平台数: {has_pre_online_cost}")
    
    # 保存结果
    output_file = base_dir / "专区接入情况统计表_含成本统计_完整版.xlsx"
    df_stats.to_excel(output_file, index=False)
    print(f"\n6. 已保存到: {output_file}")
    
    # 显示示例数据
    print("\n7. 示例数据（前5条有成本的）:")
    has_cost = df_stats[df_stats['总人工成本'] > 0]
    if len(has_cost) > 0:
        preview_cols = [df_stats.columns[2], contract_col, '总人工成本', '上线前人工成本']
        print(has_cost[preview_cols].head())
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    process_task_cost()
