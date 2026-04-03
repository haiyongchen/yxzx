# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")

# 输出到文件
with open('D:/openclaw-workspace/scripts/columns_check.txt', 'w', encoding='utf-8') as f:
    f.write("统计表列名:\n")
    for i, col in enumerate(df_stats.columns):
        f.write(f"  {i}: {col}\n")
    
    f.write("\n\n前5行数据:\n")
    f.write(df_stats.head(5).to_string())
    
    f.write("\n\n客户名称列(索引4)前20个值:\n")
    customer_col = df_stats.columns[4]
    for i, val in enumerate(df_stats[customer_col].dropna().head(20)):
        f.write(f"  {i}: {val}\n")
    
    f.write("\n\n省份列(索引5)前20个值:\n")
    province_col = df_stats.columns[5]
    for i, val in enumerate(df_stats[province_col].dropna().head(20)):
        f.write(f"  {i}: {val}\n")

print("已保存到 columns_check.txt")
