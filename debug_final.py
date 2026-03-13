# -*- coding: utf-8 -*-
"""
调试 - 查看实际匹配情况
"""
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
matched = []

for i, line in enumerate(lines):
    if line.startswith('|'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 10:
            province = cells[6] if len(cells) > 6 else ""
            # 写入文件以便查看
            if province:
                matched.append((i, province, line[:200]))

# 写入文件
with open("D:/openclaw-workspace/output/debug_all_provinces.txt", "w", encoding="utf-8") as f:
    f.write("Found %d lines with province data\n\n" % len(matched))
    for i, province, line in matched[:50]:
        f.write("Line %d, Province '%s': %s\n\n" % (i, province, line))

# 查找匹配的省份
matched_chen = []
for i, line in enumerate(lines):
    if line.startswith('|'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 10:
            province = cells[6] if len(cells) > 6 else ""
            if province in chen_provinces:
                matched_chen.append((i, province, line[:200]))

with open("D:/openclaw-workspace/output/debug_chen_provinces.txt", "w", encoding="utf-8") as f:
    f.write("Found %d lines with CHEN provinces\n\n" % len(matched_chen))
    for i, province, line in matched_chen:
        f.write("Line %d, Province '%s': %s\n\n" % (i, province, line))

print("Done! Check output files")
print("Total lines with province: %d" % len(matched))
print("Lines with CHEN provinces: %d" % len(matched_chen))
