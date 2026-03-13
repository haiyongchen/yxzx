# -*- coding: utf-8 -*-
"""
调试 - 查看单元格解析
"""
import json

# 读取文件
with open("D:/openclaw-workspace/output/doc2_sheet2.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 解析 JSON
data = json.loads(content)
text = data.get("content", "")

# 查找包含"内蒙古"的行
lines = text.split('\n')
for i, line in enumerate(lines):
    if '内蒙古' in line and line.startswith('|'):
        print("Line %d: %s" % (i, line[:300]))
        # 解析单元格
        parts = line.split('|')
        cells = [c.strip() for c in parts[1:-1]] if len(parts) > 2 and parts[0] == '' and parts[-1] == '' else [c.strip() for c in parts]
        print("Cells (%d): %s" % (len(cells), cells[:15]))
        print("Cell 6 (province): '%s'" % (cells[6] if len(cells) > 6 else "N/A"))
        print()
