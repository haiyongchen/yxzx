# -*- coding: utf-8 -*-
"""
解析腾讯文档数据，筛选陈海勇负责的 12 个省份
"""
import pandas as pd
import json
import re

# 读取文件
with open("D:/openclaw-workspace/output/doc2_sheet2.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 解析 JSON
data = json.loads(content)
text = data.get("content", "")

# 陈海勇负责的 12 个省份
chen_provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]

# 解析表格行
rows = []
for line in text.split('\n'):
    if line.startswith('|'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 10 and cells[0].isdigit():
            rows.append(cells)

# 创建 DataFrame
cols = ["序号", "专区名称", "客户名称", "系统版本", "分公司", "所属", "省份", "地市", "BU 运营", "商务", "交付", "接入日期"]
df = pd.DataFrame(rows, columns=cols[:len(rows[0]) if rows else 12])

# 筛选 12 个省份
df_filtered = df[df["省份"].isin(chen_provinces)]

# 保存
output = "D:/openclaw-workspace/output/陈海勇负责专区_最终版.xlsx"
df_filtered.to_excel(output, index=False)

print("Done: %d records" % len(df_filtered))
print("Saved to: %s" % output)
print("\nPreview:")
print(df_filtered.head(30).to_string())
