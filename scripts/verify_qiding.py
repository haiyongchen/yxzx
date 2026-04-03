# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")

# 读取结果文件
df_result = pd.read_excel(base_dir / "专区接入情况统计表_含成本统计.xlsx")

# 查找奇鼎农牧业投资有限责任公司招采平台
qiding = df_result[df_result['专区名称'].str.contains('奇鼎', na=False)]

print("奇鼎农牧业投资有限责任公司招采平台的数据:")
print(qiding[['专区名称', '合同号', '专区上线时间', '总人工成本', '上线前人工成本']].to_string())

# 验证其他示例
print("\n\n其他有成本数据的平台示例:")
has_cost = df_result[df_result['总人工成本'] > 0]
print(has_cost[['专区名称', '合同号', '总人工成本', '上线前人工成本']].head(10).to_string())
