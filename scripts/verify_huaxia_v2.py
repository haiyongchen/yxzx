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

# 将项目数转换为数字后求和
df_total[project_col] = pd.to_numeric(df_total[project_col], errors='coerce')
project_sum = df_total[df_total[platform_col].str.contains('华厦', na=False)][project_col].sum()
print(f"\n华厦专区项目数总和（转换后）: {project_sum}")

# 验证其他平台
print("\n其他平台的项目数示例:")
for platform in ['六安专区', '东海专区', '宣城交易公司专区']:
    platform_data = df_total[df_total[platform_col] == platform]
    if len(platform_data) > 0:
        project_sum = platform_data[project_col].sum()
        print(f"  {platform}: {project_sum} 个项目")
