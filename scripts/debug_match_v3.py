# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx")

# 读取收益文件
df_rev = pd.read_excel(base_dir / "e交易收益情况" / "e交易26年3月收益情况.xlsx")

print("统计表-专区名称示例:")
print(df_stats.iloc[:, 1].dropna().head(20).tolist())

print("\n收益文件-平台名称示例:")
print(df_rev.iloc[:, 3].dropna().head(20).tolist())

# 检查是否有匹配
stats_names = set(df_stats.iloc[:, 1].dropna().astype(str))
rev_names = set(df_rev.iloc[:, 3].dropna().astype(str))

common = stats_names & rev_names
print(f"\n专区名称匹配数: {len(common)}")
if len(common) > 0:
    print("匹配的名称:")
    print(list(common)[:10])
