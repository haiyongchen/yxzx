#!/usr/bin/env python3
"""
更新专区接入情况统计表.xlsx
根据专区名称匹配26年各专区收益.xlsx中的数据
"""

import pandas as pd
import os

# 文件路径
base_path = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\同步数据文件"
stats_file = os.path.join(base_path, "专区接入情况统计表.xlsx")
revenue_file = os.path.join(base_path, "26年各专区收益.xlsx")

print("正在读取文件...")

# 读取两个Excel文件
df_stats = pd.read_excel(stats_file)
df_revenue = pd.read_excel(revenue_file)

print(f"专区接入情况统计表: {len(df_stats)} 行")
print(f"26年各专区收益: {len(df_revenue)} 行")

# 查看列名
print("\n专区接入情况统计表 列名:")
print(df_stats.columns.tolist())
print("\n26年各专区收益 列名:")
print(df_revenue.columns.tolist())

# 获取专区名称列（处理空格）
stats_name_col = '      专区名称'
if stats_name_col not in df_stats.columns:
    # 尝试其他可能的列名
    for col in df_stats.columns:
        if '专区名称' in col:
            stats_name_col = col
            break

revenue_name_col = '平台名称（财经系统）'

print(f"\n使用匹配列:")
print(f"  统计表: '{stats_name_col}'")
print(f"  收益表: '{revenue_name_col}'")

# 清理数据：去除空格和换行符
df_stats[stats_name_col] = df_stats[stats_name_col].astype(str).str.strip().str.replace(r'\n', '', regex=True)
df_revenue[revenue_name_col] = df_revenue[revenue_name_col].astype(str).str.strip()

# 需要更新的列
update_cols = ['项目数', '平均订单数', '收益', '实得收益', '收益环比', '收益同比']

# 确保统计表中有这些列
for col in update_cols:
    if col not in df_stats.columns:
        df_stats[col] = None
        print(f"  添加新列: {col}")

# 匹配并更新数据
matched_count = 0
for idx, row in df_stats.iterrows():
    zone_name = row[stats_name_col]
    
    # 在收益表中查找匹配的记录
    match = df_revenue[df_revenue[revenue_name_col] == zone_name]
    
    if not match.empty:
        matched_count += 1
        # 取第一条匹配记录（假设专区名称唯一）
        revenue_row = match.iloc[0]
        
        # 更新数据
        for col in update_cols:
            if col in df_revenue.columns:
                df_stats.at[idx, col] = revenue_row[col]

print(f"\n匹配成功: {matched_count} 条记录")

# 保存更新后的文件
output_file = os.path.join(base_path, "专区接入情况统计表_已更新.xlsx")
df_stats.to_excel(output_file, index=False)

print(f"\n已保存到: {output_file}")
print("\n更新完成！")

# 显示部分更新后的数据
print("\n更新后的数据预览:")
preview_cols = [stats_name_col, '项目数', '平均订单数', '收益', '实得收益']
print(df_stats[preview_cols].head(10))
