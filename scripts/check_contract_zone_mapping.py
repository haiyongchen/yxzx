# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取统计表
df_stats = pd.read_excel(base_dir / "专区接入情况统计表.xlsx", sheet_name=0)

contract_col = df_stats.columns[0]  # A列：合同号
zone_col = df_stats.columns[2]      # C列：专区名称

print("检查多个合同号对应同一个专区名称的情况:\n")

# 查找包含分号的合同号
multi_contract = df_stats[df_stats[contract_col].astype(str).str.contains(';|；', na=False)]

print(f"有多个合同号的平台数: {len(multi_contract)}")

if len(multi_contract) > 0:
    print("\n示例数据:")
    for idx, row in multi_contract.head(10).iterrows():
        print(f"  专区名称: {row[zone_col]}")
        print(f"  合同号: {row[contract_col]}")
        print()

# 检查同一个专区名称是否有不同的合同号
print("\n按专区名称分组，查看合同号数量:")
zone_contracts = df_stats.groupby(zone_col)[contract_col].apply(lambda x: list(x.unique()))
multi_contract_zones = zone_contracts[zone_contracts.apply(len) > 1]

print(f"有多个不同合同号的专区数: {len(multi_contract_zones)}")

if len(multi_contract_zones) > 0:
    print("\n示例:")
    for zone, contracts in list(multi_contract_zones.items())[:5]:
        print(f"  {zone}: {contracts}")
