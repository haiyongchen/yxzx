# -*- coding: utf-8 -*-
"""
最终版本 - 正确解析
"""
import pandas as pd
import json

# 读取文件
with open("D:/openclaw-workspace/output/doc2_sheet2.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 解析 JSON
data = json.loads(content)
text = data.get("content", "")

# 陈海勇负责的 12 个省份
chen_provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]

# 查找所有行
lines = text.split('\n')
rows = []

for line in lines:
    if line.startswith('|'):
        # 按 | 分割，保留空单元格
        parts = line.split('|')
        # 过滤掉首尾空字符串
        cells = [c.strip() for c in parts[1:-1]] if parts[0] == '' and parts[-1] == '' else [c.strip() for c in parts]
        
        # 查找包含省份的行（第 7 列，索引 6）
        if len(cells) >= 10:
            province = cells[6] if len(cells) > 6 else ""
            if province in chen_provinces:
                rows.append({
                    "序号": cells[0],
                    "专区名称": cells[1] if len(cells) > 1 else "",
                    "客户名称": cells[2] if len(cells) > 2 else "",
                    "系统版本": cells[3] if len(cells) > 3 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": province,
                    "地市": cells[7] if len(cells) > 7 else "",
                    "BU 运营": cells[8] if len(cells) > 8 else "",
                    "商务": cells[9] if len(cells) > 9 else "",
                    "交付": cells[10] if len(cells) > 10 else "",
                    "接入日期": cells[11] if len(cells) > 11 else "",
                })

# 创建 DataFrame
df = pd.DataFrame(rows)

# 保存
output = "D:/openclaw-workspace/output/陈海勇负责专区_最终版.xlsx"
df.to_excel(output, index=False)

print("Done: %d records" % len(df))
print("Saved to: %s" % output)

if len(df) > 0:
    print("\n按省份统计:")
    print(df["省份"].value_counts())
    print("\nPreview:")
    print(df.head(30).to_string())
