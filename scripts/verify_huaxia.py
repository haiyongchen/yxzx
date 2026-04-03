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

# 查找华厦专区的数据
platform_col = df_total.columns[3]  # D列：平台名称
project_col = df_total.columns[5]   # F列：项目数

print(f"\n查找平台名称列: {platform_col}")
print(f"项目数列: {project_col}")

# 查找包含"华厦"的数据
huaxia_data = df_total[df_total[platform_col].str.contains('华厦', na=False)]
print(f"\n华厦专区的数据:")
print(huaxia_data[[platform_col, project_col]].to_string())

# 计算项目数总和
project_sum = huaxia_data[project_col].sum()
print(f"\n华厦专区项目数总和: {project_sum}")
