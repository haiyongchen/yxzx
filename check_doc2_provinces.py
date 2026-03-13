# -*- coding: utf-8 -*-
"""
检查文档 2 中实际包含的省份和分公司
"""
from pathlib import Path
from collections import Counter

doc2_file = Path("D:/openclaw-workspace/output/doc2_content.txt")
with open(doc2_file, "r", encoding="utf-8") as f:
    content = f.read()

# 查找所有省份
provinces = ["浙江", "江苏", "安徽", "广东", "江西", "云南", "贵州", "四川", "重庆", "湖南", "广西", "海南", "甘肃", "宁夏", "陕西", "新疆", "内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "山东", "山西", "北京", "天津", "上海", "福建"]

print("文档 2 中包含的省份:")
print("=" * 80)

lines = content.split('\n')
province_count = Counter()

for line in lines:
    for province in provinces:
        if province in line and '|' in line:
            province_count[province] += 1
            break

# 打印统计
for province, count in province_count.most_common(30):
    print(f"{province}: {count} 次")

print(f"\n总计匹配到 {sum(province_count.values())} 行包含省份信息")
