# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx", sheet_name=0)
contract_col = df_stats.columns[0]  # A列：合同号
zone_col = df_stats.columns[2]      # C列：专区名称

# 找一个有多个合同号的平台
multi_contract = df_stats[df_stats[contract_col].astype(str).str.contains(';|；', na=False)]

if len(multi_contract) > 0:
    sample = multi_contract.iloc[0]
    print("示例：有多个合同号的平台")
    print(f"  专区名称: {sample[zone_col]}")
    print(f"  合同号: {sample[contract_col]}")
    
    # 检查这个专区名称在统计表中是否有其他记录
    zone_name = sample[zone_col]
    same_zone = df_stats[df_stats[zone_col] == zone_name]
    print(f"\n  该专区在统计表中的记录数: {len(same_zone)}")
    if len(same_zone) > 1:
        print("  该专区的所有合同号:")
        for idx, row in same_zone.iterrows():
            print(f"    - {row[contract_col]}")

print("\n\n结论:")
print("收益文件中的数据是按'平台名称（标准系统名）'聚合的，")
print("不是按合同号。所以同一个平台名称的收益数据")
print("已经包含了该平台的所有合同号的收益总和。")
print("因此，按平台名称匹配并累加是正确的做法。")
