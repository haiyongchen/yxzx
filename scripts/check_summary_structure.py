# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
summary_file = base_dir / "专区信息汇总表_按省份分类.xlsx"

# 尝试读取所有sheet
xl = pd.ExcelFile(summary_file)
print(f"Sheet names: {xl.sheet_names}")

# 读取第一个sheet
df = pd.read_excel(summary_file, sheet_name=0)
print(f"\n总行数: {len(df)}")
print(f"\n列名: {df.columns.tolist()}")
print(f"\n前5行数据:")
print(df.head())
