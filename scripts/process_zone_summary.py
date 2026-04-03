# -*- coding: utf-8 -*-
"""
处理专区信息汇总表_按省份分类.xlsx
添加收益计算和成本计算
"""

import pandas as pd
from pathlib import Path
import numpy as np
import re

def parse_percentage(val):
    """解析百分比字符串为数值"""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    match = re.search(r'[-+]?[\d,]+\.?\d*', val_str)
    if match:
        num_str = match.group().replace(',', '')
        try:
            return float(num_str)
        except:
            return np.nan
    return np.nan

def process_zone_summary():
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    summary_file = base_dir / "专区信息汇总表_按省份分类.xlsx"
    revenue_dir = base_dir / "e交易收益情况"
    task_file = base_dir / "任务使用表.xls"
    
    print("=" * 60)
    print("开始处理专区信息汇总表")
    print("=" * 60)
    
    # 读取汇总表
    print(f"\n1. 读取汇总表...")
    df_summary = pd.read_excel(summary_file, sheet_name=0)
    print(f"   汇总表行数: {len(df_summary)}")
    print(f"   汇总表列名: {df_summary.columns.tolist()}")
    
    # 找到专区名称列
    zone_col = None
    for col in df_summary.columns:
        if '专区' in str(col) or '名称' in str(col):
            zone_col = col
            print(f"   专区名称列: {col}")
            break
    
    if zone_col is None:
        zone_col = df_summary.columns[0]
        print(f"   使用第一列作为专区名称列: {zone_col}")
    
    # 获取收益文件
    files = sorted([f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")])
    file_2025 = files[0]
    file_2026_month = files[1]
    file_2026_total = files[2]
    file_total = files[3]
    
    print(f"\n2. 找到收益文件:")
    print(f"   2025年: {file_2025.name}")
    print(f"   2026年3月: {file_2026_month.name}")
    print(f"   2026年截至3月25日: {file_2026_total.name}")
    print(f"   总收益截至2026年3月25日: {file_total.name}")
    
    # 初始化收益列
    print("\n3. 初始化收益列...")
    df_summary['e交易26年3月_当月收益'] = 0.0
    df_summary['e交易26年3月_当月收益同比'] = np.nan
    df_summary['e交易26年3月_当月收益环比'] = np.nan
    df_summary['e交易26年_26年总收益'] = 0.0
    df_summary['e交易25年_25年总收益'] = 0.0
    df_summary['e交易总收益_总收益'] = 0.0
    df_summary['e交易总收益_总项目数'] = 0
    
    # 处理2026年3月收益数据
    print("\n4. 处理2026年3月收益数据...")
    df_month = pd.read_excel(file_2026_month, sheet_name=0)
    platform_col = df_month.columns[3]
    revenue_col = df_month.columns[8]
    yoy_col = df_month.columns[10]
    mom_col = df_month.columns[9]
    
    month_summary = df_month.groupby(platform_col).agg({
        revenue_col: 'sum',
        yoy_col: 'first',
        mom_col: 'first'
    })
    
    match_count = 0
    for idx, row in df_summary.iterrows():
        zone_name = str(row[zone_col]).strip()
        if zone_name in month_summary.index:
            df_summary.at[idx, 'e交易26年3月_当月收益'] = month_summary.loc[zone_name, revenue_col]
            df_summary.at[idx, 'e交易26年3月_当月收益同比'] = parse_percentage(month_summary.loc[zone_name, yoy_col])
            df_summary.at[idx, 'e交易26年3月_当月收益环比'] = parse_percentage(month_summary.loc[zone_name, mom_col])
            match_count += 1
    print(f"   匹配成功: {match_count} 条")
    
    # 处理2026年总收益数据
    print("\n5. 处理2026年总收益数据...")
    df_2026 = pd.read_excel(file_2026_total, sheet_name=0)
    platform_col = df_2026.columns[3]
    revenue_col = df_2026.columns[8]
    summary_2026 = df_2026.groupby(platform_col)[revenue_col].sum()
    
    match_count = 0
    for idx, row in df_summary.iterrows():
        zone_name = str(row[zone_col]).strip()
        if zone_name in summary_2026.index:
            df_summary.at[idx, 'e交易26年_26年总收益'] = summary_2026[zone_name]
            match_count += 1
    print(f"   匹配成功: {match_count} 条")
    
    # 处理2025年收益数据
    print("\n6. 处理2025年收益数据...")
    df_2025 = pd.read_excel(file_2025, sheet_name=0)
    platform_col = df_2025.columns[3]
    revenue_col = df_2025.columns[8]
    summary_2025 = df_2025.groupby(platform_col)[revenue_col].sum()
    
    match_count = 0
    for idx, row in df_summary.iterrows():
        zone_name = str(row[zone_col]).strip()
        if zone_name in summary_2025.index:
            df_summary.at[idx, 'e交易25年_25年总收益'] = summary_2025[zone_name]
            match_count += 1
    print(f"   匹配成功: {match_count} 条")
    
    # 处理总收益数据
    print("\n7. 处理总收益数据...")
    df_total_rev = pd.read_excel(file_total, sheet_name=0)
    platform_col = df_total_rev.columns[3]
    revenue_col = df_total_rev.columns[8]
    project_col = df_total_rev.columns[5]
    
    # 先将项目数转换为数字
    df_total_rev[project_col] = pd.to_numeric(df_total_rev[project_col], errors='coerce')
    total_revenue = df_total_rev.groupby(platform_col)[revenue_col].sum()
    total_projects = df_total_rev.groupby(platform_col)[project_col].sum()
    
    match_count = 0
    for idx, row in df_summary.iterrows():
        zone_name = str(row[zone_col]).strip()
        if zone_name in total_revenue.index:
            df_summary.at[idx, 'e交易总收益_总收益'] = total_revenue[zone_name]
            if zone_name in total_projects.index:
                df_summary.at[idx, 'e交易总收益_总项目数'] = int(total_projects[zone_name])
            match_count += 1
    print(f"   匹配成功: {match_count} 条")
    
    # 读取任务使用表并处理成本
    print("\n8. 处理成本数据...")
    df_task = pd.read_excel(task_file, sheet_name=0)
    task_contract_col = df_task.columns[10]  # K列：合同编号
    task_start_col = df_task.columns[5]      # F列：实际开始时间
    task_cost_col = df_task.columns[8]       # I列：实际人工成本
    
    # 找到合同号列和上线时间列
    contract_col = None
    online_time_col = None
    for col in df_summary.columns:
        col_str = str(col)
        if '合同' in col_str:
            contract_col = col
            print(f"   合同号列: {col}")
        if '上线' in col_str and '时间' in col_str:
            online_time_col = col
            print(f"   上线时间列: {col}")
    
    if contract_col is None:
        print("   未找到合同号列，跳过成本计算")
    else:
        df_summary['总人工成本'] = 0.0
        df_summary['上线前人工成本'] = 0.0
        
        # 按合同编号分组统计总人工成本
        total_cost_by_contract = df_task.groupby(task_contract_col)[task_cost_col].sum()
        
        match_count = 0
        for idx, row in df_summary.iterrows():
            contract_no = str(row[contract_col]).strip()
            online_time = row[online_time_col] if online_time_col else None
            
            # 处理多个合同号（用分号分隔）
            contract_list = [c.strip() for c in contract_no.replace('；', ';').split(';') if c.strip()]
            
            total_cost = 0.0
            pre_online_cost = 0.0
            has_match = False
            
            for single_contract in contract_list:
                if single_contract in total_cost_by_contract.index:
                    total_cost += total_cost_by_contract[single_contract]
                    has_match = True
                    
                    # 统计上线前人工成本
                    if online_time_col and pd.notna(online_time):
                        try:
                            if not isinstance(online_time, pd.Timestamp):
                                online_time = pd.to_datetime(online_time)
                            task_start_times = pd.to_datetime(df_task[task_start_col], errors='coerce')
                            task_records = df_task[
                                (df_task[task_contract_col] == single_contract) & 
                                (task_start_times <= online_time) &
                                (task_start_times.notna())
                            ]
                            if len(task_records) > 0:
                                pre_online_cost += task_records[task_cost_col].sum()
                        except:
                            pass
            
            if has_match:
                df_summary.at[idx, '总人工成本'] = total_cost
                df_summary.at[idx, '上线前人工成本'] = pre_online_cost
