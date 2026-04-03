# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")
print("统计表平台列示例:")
platform_col = None
for col in df_stats.columns:
    if '平台' in str(col):
        platform_col = col
        break

if platform_col:
    print(f"平台列名: {platform_col}")
    print("前10个平台名称:")
    print(df_stats[platform_col].head(10).tolist())

# 读取收益文件
df_rev = pd.read_excel(base_dir / "e交易收益情况" / "e交易26年3月收益情况.xlsx")
print("\n收益文件列名:")
print(df_rev.columns.tolist())
print("\n前10个平台名称:")
print(df_rev.iloc[:10, 3].tolist())

# 检查是否有匹配
stats_platforms = set(df_stats[platform_col].dropna().astype(str))
rev_platforms = set(df_rev.iloc[:, 3].dropna().astype(str))

print(f"\n统计表平台数: {len(stats_platforms)}")
print(f"收益文件平台数: {len(rev_platforms)}")

# 找交集
common = stats_platforms & rev_platforms
print(f"\n匹配的平台数: {len(common)}")
if len(common) > 0:
    print("匹配的平台示例:")
    print(list(common)[:5])
else:
    print("没有匹配的平台，检查平台名称格式...")
    print("\n统计表前5个平台:")
    print(list(stats_platforms)[:5])
    print("\n收益文件前5个平台:")
    print(list(rev_platforms)[:5])
