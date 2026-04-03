# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")
print("统计表所有列名:")
for i, col in enumerate(df_stats.columns):
    print(f"  {i}: {col}")

print("\n统计表前3行所有列:")
print(df_stats.head(3))

# 读取收益文件
df_rev = pd.read_excel(base_dir / "e交易收益情况" / "e交易26年3月收益情况.xlsx")
print("\n\n收益文件所有列名:")
for i, col in enumerate(df_rev.columns):
    print(f"  {i}: {col}")

print("\n收益文件前3行:")
print(df_rev.head(3))
