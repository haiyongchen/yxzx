# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")

print("统计表所有列名:")
for i, col in enumerate(df_stats.columns):
    print(f"  {i}: {col}")

print("\n\n统计表前3行数据（所有列）:")
print(df_stats.head(3).to_string())

print("\n\n检查各列是否有中文内容:")
for i, col in enumerate(df_stats.columns):
    sample = df_stats[col].dropna().head(5).tolist()
    has_chinese = any('\u4e00' <= str(c) <= '\u9fff' for c in str(sample))
    print(f"  {i} {col}: {'有中文' if has_chinese else '无中文'} - 示例: {sample[:3]}")
