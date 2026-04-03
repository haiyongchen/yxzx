# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
revenue_dir = base_dir / "e交易收益情况"

# 读取总收益文件
df_total = pd.read_excel(revenue_dir / "e交易总收益情况（截至2026年3月25日）.xlsx", sheet_name=0)

platform_col = df_total.columns[3]  # D列：平台名称
project_col = df_total.columns[5]   # F列：项目数

# 查找华厦专区的数据
huaxia_data = df_total[df_total[platform_col].str.contains('华厦', na=False)]
print("华厦专区的原始数据:")
print(huaxia_data[[platform_col, project_col]])

print("\n项目数数据类型:")
print(huaxia_data[project_col].dtype)

print("\n项目数值:")
for idx, val in huaxia_data[project_col].items():
    print(f"  行{idx}: {val} (类型: {type(val)})")
