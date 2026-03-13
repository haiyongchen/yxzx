# -*- coding: utf-8 -*-
"""
快速提取陈海勇负责的 12 个省份的专区 - 最快版本
"""
import re
from pathlib import Path

# 陈海勇负责的 12 个省份
chen_provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]

# 读取文档
doc_file = Path("D:/openclaw-workspace/output/doc2_sheet2.txt")
with open(doc_file, "r", encoding="utf-8") as f:
    content = f.read()

# 快速匹配
matched = []
for line in content.split('\n'):
    if line.startswith('|') and any(p in line for p in chen_provinces):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 7 and cells[0].isdigit():
            matched.append({
                "序号": cells[0],
                "专区名称": cells[1] if len(cells) > 1 else "",
                "客户名称": cells[2] if len(cells) > 2 else "",
                "系统版本": cells[3] if len(cells) > 3 else "",
                "分公司": cells[4] if len(cells) > 4 else "",
                "省份": cells[6] if len(cells) > 6 else "",
                "地市": cells[7] if len(cells) > 7 else "",
                "商务": cells[9] if len(cells) > 9 else "",
            })

print("Found %d zones" % len(matched))
print("\n" + "=" * 120)

# 按省份统计
from collections import Counter
province_count = Counter([m["省份"] for m in matched])
print("\nBy Province:")
for p, c in province_count.most_common():
    print("  %s: %d" % (p, c))

# 保存 Excel
import pandas as pd
df = pd.DataFrame(matched)
output_file = "D:/openclaw-workspace/output/陈海勇负责专区_最终版.xlsx"
df.to_excel(output_file, index=False)
print("\n[OK] Excel saved to: %s" % output_file)
print("Total: %d records" % len(df))

# 打印预览
print("\n" + "=" * 120)
print("Preview (first 20):")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.head(20).to_string(index=False))
