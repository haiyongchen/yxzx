# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx", sheet_name=0)

print("统计表列名:")
for i, col in enumerate(df_stats.columns):
    print(f"  {i}: {col}")

# 检查前几行
print("\n前5行数据:")
print(df_stats.head())

# 查找专区码和专区名称的对应关系
zone_code_col = df_stats.columns[1]  # 专区码
zone_name_col = df_stats.columns[2]  # 专区名称

print(f"\n专区码示例: {df_stats[zone_code_col].dropna().head(10).tolist()}")
print(f"专区名称示例: {df_stats[zone_name_col].dropna().head(10).tolist()}")

# 创建映射表
mapping = dict(zip(df_stats[zone_code_col].dropna().astype(str), 
                   df_stats[zone_name_col].dropna().astype(str)))
print(f"\n映射表条目数: {len(mapping)}")
print("映射表示例:")
for code, name in list(mapping.items())[:10]:
    print(f"  {code} -> {name}")
