# -*- coding: utf-8 -*-
"""
快速提取陈海勇负责的 12 个省份的专区 - 优化版
"""
import re
from pathlib import Path

# 陈海勇负责的 12 个省份
chen_provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]

# 读取文档
doc_file = Path("D:/openclaw-workspace/output/doc2_sheet2.txt")
with open(doc_file, "r", encoding="utf-8") as f:
    content = f.read()

# 快速匹配包含省份的行
matched_lines = []
for line in content.split('\n'):
    if line.startswith('|') and any(p in line for p in chen_provinces):
        matched_lines.append(line)

print("Found %d lines" % len(matched_lines))
print("\n" + "=" * 100)

# 打印前 20 条
for i, line in enumerate(matched_lines[:20]):
    print("%d: %s" % (i+1, line[:150]))

print("\nTotal: %d lines" % len(matched_lines))
