# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")

# 检查客户名称列（索引4）
print("客户名称列示例:")
customer_col = df_stats.columns[4]
print(f"列名: {customer_col}")
print(f"前20个客户名称:")
print(df_stats[customer_col].dropna().head(20).tolist())

# 同时检查省份列
print("\n\n省份列示例:")
province_col = df_stats.columns[5]
print(f"列名: {province_col}")
print(f"前20个省份:")
print(df_stats[province_col].dropna().head(20).tolist())

# 检查是否有中文
print("\n\n检查客户名称是否有中文:")
samples = df_stats[customer_col].dropna().head(20).tolist()
for s in samples:
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in str(s))
    print(f"  {s}: {'有中文' if has_chinese else '无中文'}")
