# -*- coding: utf-8 -*-
"""
从腾讯文档数据中筛选陈海勇负责的所有专区明细
"""
import pandas as pd
import re
from pathlib import Path

# 陈海勇负责的分公司关键词
chen_keywords = {
    "华北区": ["呼和浩特", "沈阳", "长春"],
    "华中区": ["石家庄", "武汉", "郑州"],
    "西北区": ["乌鲁木齐"],
    "政务华东区": ["北京", "天津"],
    "交易华东区": ["济南"]
}

# 读取文档内容
doc_file = Path("D:/openclaw-workspace/output/doc1_content.txt")
with open(doc_file, "r", encoding="utf-8") as f:
    content = f.read()

# 解析表格行
lines = content.split('\n')
all_rows = []

for line in lines:
    if '|' in line and len(line) > 30:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 5:
            all_rows.append(cells)

print(f"解析到 {len(all_rows)} 行表格数据")

# 筛选陈海勇负责的专区
matched_zones = []

for row in all_rows:
    row_text = ' | '.join(row)
    
    # 检查是否包含陈海勇负责的分公司关键词
    for region, keywords in chen_keywords.items():
        for keyword in keywords:
            if keyword in row_text:
                matched_zones.append({
                    "大区": region,
                    "匹配关键词": keyword,
                    "数据": row
                })
                break

print(f"\n匹配到 {len(matched_zones)} 条陈海勇负责的专区数据")

# 保存结果
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("陈海勇负责专区明细\n")
    f.write("=" * 100 + "\n\n")
    
    for item in matched_zones:
        f.write(f"大区：{item['大区']} | 匹配关键词：{item['匹配关键词']}\n")
        f.write(f"数据：{' | '.join(item['数据'][:15])}\n")
        f.write("-" * 100 + "\n")

print(f"\n结果已保存：{output_file}")

# 打印预览
print("\n" + "=" * 100)
print("陈海勇负责专区明细（前 20 条）")
print("=" * 100)
for i, item in enumerate(matched_zones[:20]):
    print(f"\n{i+1}. {item['大区']} - {item['匹配关键词']}")
    print(f"   {' | '.join(item['数据'][:10])}")
