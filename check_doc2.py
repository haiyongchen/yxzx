# -*- coding: utf-8 -*-
"""
检查文档 2 的数据格式并优化匹配
"""
from pathlib import Path

doc2_file = Path("D:/openclaw-workspace/output/doc2_content.txt")
with open(doc2_file, "r", encoding="utf-8") as f:
    content = f.read()

# 查找包含陈海勇负责区域的行
keywords = ["内蒙古", "辽宁", "吉林", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "沈阳", "长春", "哈尔滨", "石家庄", "武汉", "郑州", "乌鲁木齐", "济南"]

print("查找文档 2 中包含陈海勇负责区域的行:")
print("=" * 80)

lines = content.split('\n')
found_lines = []

for i, line in enumerate(lines):
    for kw in keywords:
        if kw in line and '|' in line:
            found_lines.append((i+1, line[:200]))
            break

print(f"找到 {len(found_lines)} 行包含关键词:\n")
for line_num, line_content in found_lines[:30]:
    print(f"行{line_num}: {line_content}...")
