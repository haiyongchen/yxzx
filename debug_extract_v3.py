# -*- coding: utf-8 -*-
"""
调试 - 查看实际数据 - 写入文件
"""
import json

# 读取文件
with open("D:/openclaw-workspace/output/doc2_sheet2.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 解析 JSON
data = json.loads(content)
text = data.get("content", "")

print("Content length:", len(text))

# 查找包含数字开头的行
lines = text.split('\n')
found_lines = []
for i, line in enumerate(lines):
    if line.startswith('|29|') or line.startswith('|73|') or line.startswith('|85|'):
        found_lines.append((i, line[:300]))

# 写入文件
with open("D:/openclaw-workspace/output/debug_lines.txt", "w", encoding="utf-8") as f:
    f.write("Content length: %d\n\n" % len(text))
    f.write("Found %d lines\n\n" % len(found_lines))
    for i, line in found_lines[:10]:
        f.write("Line %d: %s\n\n" % (i, line))

# 查找包含省份的行
provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]
found_provinces = []
for line in lines:
    for p in provinces:
        if p in line:
            found_provinces.append((p, line[:200]))
            break

with open("D:/openclaw-workspace/output/debug_provinces.txt", "w", encoding="utf-8") as f:
    f.write("Found %d lines with provinces\n\n" % len(found_provinces))
    for p, line in found_provinces[:20]:
        f.write("Province %s: %s\n\n" % (p, line))

print("Done! Check output/debug_lines.txt and output/debug_provinces.txt")
