#!/usr/bin/env python3
"""
e交易数据处理主脚本
1. 执行原有的数据处理
2. 更新专区接入情况统计表（直接修改原文件）
3. 在收益表中标识未匹配的数据
"""

import subprocess
import pandas as pd
import os
import sys

def run_original_script():
    """执行原有的 Python 脚本"""
    script_path = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\专区统计代码\main_auto_with_email.py"
    print(f"执行原脚本: {script_path}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print("原脚本输出:")
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    return result.returncode == 0

def update_revenue_data():
    """更新专区接入情况统计表（直接修改原文件）"""
    base_path = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\同步数据文件"
    stats_file = os.path.join(base_path, "专区接入情况统计表.xlsx")
    revenue_file = os.path.join(base_path, "26年各专区收益.xlsx")
    
    print("\n正在更新收益数据...")
    
    # 读取两个Excel文件
    df_stats = pd.read_excel(stats_file)
    df_revenue = pd.read_excel(revenue_file)
    
    print(f"专区接入情况统计表: {len(df_stats)} 行")
    print(f"26年各专区收益: {len(df_revenue)} 行")
    
    # 获取专区名称列
    stats_name_col = '专区名称'
    revenue_name_col = '平台名称（财经系统）'
    
    # 清理数据
    df_stats[stats_name_col] = df_stats[stats_name_col].astype(str).str.strip().str.replace(r'\n', '', regex=True)
    df_revenue[revenue_name_col] = df_revenue[revenue_name_col].astype(str).str.strip()
    
    # 需要更新的列
    update_cols = ['项目数', '平均订单数', '收益', '实得收益', '收益环比', '收益同比']
    
    # 确保统计表中有这些列，并设置为 object 类型以容纳各种数据
    for col in update_cols:
        if col not in df_stats.columns:
            df_stats[col] = pd.Series(dtype='object')
        else:
            # 转换为 object 类型以避免数据类型冲突
            df_stats[col] = df_stats[col].astype('object')
    
    # 在收益表中添加"匹配状态"列
    if '匹配状态' not in df_revenue.columns:
        df_revenue['匹配状态'] = '未匹配'
    else:
        df_revenue['匹配状态'] = '未匹配'  # 重置所有为未匹配
    
    # 匹配并更新数据
    matched_count = 0
    unmatched_in_stats = []
    
    for idx, row in df_stats.iterrows():
        zone_name = row[stats_name_col]
        match = df_revenue[df_revenue[revenue_name_col] == zone_name]
        
        if not match.empty:
            matched_count += 1
            revenue_row = match.iloc[0]
            revenue_idx = match.index[0]
            
            # 更新统计表数据
            for col in update_cols:
                if col in df_revenue.columns:
                    df_stats.at[idx, col] = revenue_row[col]
            
            # 在收益表中标记为已匹配
            df_revenue.at[revenue_idx, '匹配状态'] = '已匹配'
        else:
            # 记录未匹配的专区
            unmatched_in_stats.append(zone_name)
    
    print(f"匹配成功: {matched_count} 条记录")
    print(f"未匹配: {len(unmatched_in_stats)} 条记录")
    
    # 保存更新后的统计表（覆盖原文件）
    df_stats.to_excel(stats_file, index=False)
    print(f"已更新统计表: {stats_file}")
    
    # 保存更新后的收益表（覆盖原文件，包含匹配状态）
    df_revenue.to_excel(revenue_file, index=False)
    print(f"已更新收益表（含匹配状态）: {revenue_file}")
    
    # 输出未匹配的专区名称（前10个）
    if unmatched_in_stats:
        print("\n未匹配的专区（前10个）:")
        for name in unmatched_in_stats[:10]:
            print(f"  - {name}")
    
    return True

def main():
    print("=" * 60)
    print("e交易数据处理任务")
    print("=" * 60)
    
    # 1. 执行原脚本
    success1 = run_original_script()
    
    # 2. 更新收益数据
    success2 = update_revenue_data()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("任务执行成功！")
    else:
        print("任务执行完成，但可能有部分步骤失败")
    print("=" * 60)
    
    return 0 if (success1 and success2) else 1

if __name__ == "__main__":
    sys.exit(main())
