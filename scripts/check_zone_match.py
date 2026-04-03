# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取汇总表
summary_file = base_dir / "专区信息汇总表_按省份分类.xlsx"
xl = pd.ExcelFile(summary_file)
all_sheets = []
for sheet_name in xl.sheet_names:
    df_sheet = pd.read_excel(summary_file, sheet_name=sheet_name)
    if len(df_sheet) > 0:
        all_sheets.append(df_sheet)
df_summary = pd.concat(all_sheets, ignore_index=True)

zone_col_summary = df_summary.columns[1]  # 专区名称
print("汇总表中的专区名称示例:")
print(df_summary[zone_col_summary].dropna().head(20).tolist())

# 读取收益文件
revenue_dir = base_dir / "e交易收益情况"
df_total = pd.read_excel(revenue_dir / "e交易总收益情况（截至2026年3月25日）.xlsx", sheet_name=0)
zone_col_revenue = df_total.columns[3]

print("\n收益文件中的平台名称示例:")
print(df_total[zone_col_revenue].dropna().head(20).tolist())

# 检查匹配情况
summary_zones = set(df_summary[zone_col_summary].dropna().astype(str))
revenue_zones = set(df_total[zone_col_revenue].dropna().astype(str))

common = summary_zones & revenue_zones
print(f"\n汇总表中的专区数: {len(summary_zones)}")
print(f"收益文件中的平台数: {len(revenue_zones)}")
print(f"匹配的平台数: {len(common)}")

if len(common) > 0:
    print("\n匹配的平台示例:")
    print(list(common)[:10])
else:
    print("\n没有匹配的平台")
    print("\n汇总表独有的平台示例:")
    print(list(summary_zones)[:10])
    print("\n收益文件独有的平台示例:")
    print(list(revenue_zones)[:10])
