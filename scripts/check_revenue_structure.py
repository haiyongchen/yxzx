# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
revenue_dir = base_dir / "e交易收益情况"

# 读取总收益文件
df_total = pd.read_excel(revenue_dir / "e交易总收益情况（截至2026年3月25日）.xlsx", sheet_name=0)

print("总收益文件列名:")
for i, col in enumerate(df_total.columns):
    print(f"  {i}: {col}")

# 查看是否有合同号列
print("\n前5行数据:")
print(df_total.head())

# 查看平台名称列的唯一值数量
platform_col = df_total.columns[3]
print(f"\n平台名称列({platform_col})的唯一值数量: {df_total[platform_col].nunique()}")
print(f"总行数: {len(df_total)}")

# 查看是否有重复的平台名称
duplicates = df_total[df_total.duplicated(subset=[platform_col], keep=False)]
print(f"\n有重复平台名称的行数: {len(duplicates)}")
if len(duplicates) > 0:
    print("\n重复的平台名称示例:")
    print(duplicates[[platform_col]].value_counts().head(10))
