# -*- coding: utf-8 -*-
"""
调试 - 查看实际数据
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

# 查找包含省份的行
print("Searching for provinces...")
for line in text.split('\n'):
    for province in chen_provinces:
        if province in line:
            print(f"Found '{province}': {line[:200]}")
            # 解析单元格
            cells = [c.strip() for c in line.split('|') if c.strip()]
            print(f"Cells ({len(cells)}): {cells[:15]}")
            print()
            break
