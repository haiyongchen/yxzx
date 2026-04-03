# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
revenue_dir = base_dir / "e交易收益情况"

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx", sheet_name=0)
zone_col_stats = df_stats.columns[2]  # C列：专区名称

# 读取总收益文件
df_total = pd.read_excel(revenue_dir / "e交易总收益情况（截至2026年3月25日）.xlsx", sheet_name=0)
zone_col_revenue = df_total.columns[3]  # D列：平台名称

print("收益文件中的平台名称示例:")
print(df_total[zone_col_revenue].unique()[:20])

print("\n\n统计表中的专区名称示例:")
print(df_stats[zone_col_stats].unique()[:20])

# 检查匹配情况
print("\n\n匹配检查:")
stats_zones = set(df_stats[zone_col_stats].dropna().astype(str))
revenue_zones = set(df_total[zone_col_revenue].dropna().astype(str))

common = stats_zones & revenue_zones
print(f"统计表中的专区数: {len(stats_zones)}")
print(f"收益文件中的平台数: {len(revenue_zones)}")
print(f"匹配的平台数: {len(common)}")

# 检查未匹配的平台
unmatched_stats = stats_zones - revenue_zones
unmatched_revenue = revenue_zones - stats_zones

print(f"\n统计表中有但收益文件中没有的平台数: {len(unmatched_stats)}")
if len(unmatched_stats) > 0:
    print("示例:", list(unmatched_stats)[:10])

print(f"\n收益文件中有但统计表中没有的平台数: {len(unmatched_revenue)}")
if len(unmatched_revenue) > 0:
    print("示例:", list(unmatched_revenue)[:10])
