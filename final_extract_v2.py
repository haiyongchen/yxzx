# -*- coding: utf-8 -*-
"""
解析腾讯文档数据，筛选陈海勇负责的 12 个省份 - 最终版
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

# 查找包含省份的行 (来自 25 年新开专区表格)
rows = []
for line in text.split('\n'):
    if line.startswith('|'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        # 检查是否有省份信息（第 7 列，索引 6）
        if len(cells) >= 10:
            province = cells[6] if len(cells) > 6 else ""
            if province in chen_provinces and cells[0].isdigit():
                rows.append({
                    "序号": cells[0],
                    "专区名称": cells[1] if len(cells) > 1 else "",
                    "客户名称": cells[2] if len(cells) > 2 else "",
                    "系统版本": cells[3] if len(cells) > 3 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": cells[6] if len(cells) > 6 else "",
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
print("\n按省份统计:")
print(df["省份"].value_counts())
print("\nPreview:")
print(df.head(30).to_string())
