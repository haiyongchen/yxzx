# -*- coding: utf-8 -*-
"""
最终版：合并两个腾讯文档的数据，生成陈海勇负责的所有专区明细
"""
import pandas as pd
from pathlib import Path

# 陈海勇负责的区域映射（根据架构图）
chen_regions = {
    "华北区": ["呼和浩特", "沈阳", "长春", "华北", "内蒙古", "辽宁", "吉林", "黑龙江"],
    "华中区": ["石家庄", "武汉", "郑州", "华中", "河北", "湖北", "河南"],
    "西北区": ["乌鲁木齐", "西北", "新疆", "甘肃", "青海", "宁夏", "陕西"],
    "政务华东区": ["北京", "天津"],
    "交易华东区": ["济南", "华东分公司", "山东"]
}

def match_region(text):
    """匹配大区"""
    if not text or text == "#ERROR!":
        return None
    
    for region, keywords in chen_regions.items():
        for kw in keywords:
            if kw in text:
                return region
    return None

# 读取文档 1
doc1_file = Path("D:/openclaw-workspace/output/doc1_content.txt")
with open(doc1_file, "r", encoding="utf-8") as f:
    doc1_content = f.read()

# 读取文档 2
doc2_file = Path("D:/openclaw-workspace/output/doc2_content.txt")
with open(doc2_file, "r", encoding="utf-8") as f:
    doc2_content = f.read()

# 解析文档 1（专区管控表）
print("=" * 80)
print("解析文档 1：01-新点电子交易专区&项目跟进表（重要）")
print("=" * 80)

doc1_lines = doc1_content.split('\n')
doc1_zones = []

for line in doc1_lines:
    if '|' in line and len(line) > 50:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 10:
            row_text = ' | '.join(cells)
            region = match_region(row_text)
            
            if region and '分公司' not in cells[0] and '#ERROR!' not in cells[0]:
                doc1_zones.append({
                    "来源": "文档 1-专区管控表",
                    "大区": region,
                    "专区码": cells[1] if len(cells) > 1 else "",
                    "专区名称": cells[2] if len(cells) > 2 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": cells[5] if len(cells) > 5 else "",
                    "地市": cells[6] if len(cells) > 6 else "",
                    "商务": cells[10] if len(cells) > 10 else "",
                    "专区状态": cells[14] if len(cells) > 14 else "",
                })

print(f"文档 1 匹配到 {len(doc1_zones)} 条数据")

# 解析文档 2（25 年新开专区表）
print("\n解析文档 2：25 年新开专区表")
print("=" * 80)

doc2_lines = doc2_content.split('\n')
doc2_zones = []
in_25_new_table = False

for line in doc2_lines:
    if '25 年新开专区' in line:
        in_25_new_table = True
        continue
    
    if in_25_new_table and '|' in line and len(line) > 50:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        
        # 检测表格结束
        if len(cells) > 0 and cells[0] in ['序号', '注', '专区推进']:
            continue
        
        if len(cells) >= 7:
            row_text = ' | '.join(cells)
            region = match_region(row_text)
            
            # 检查是否是数据行（序号是数字）
            if region and len(cells) > 0 and cells[0].isdigit():
                doc2_zones.append({
                    "来源": "文档 2-25 年新开专区",
                    "大区": region,
                    "专区名称": cells[1] if len(cells) > 1 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": cells[6] if len(cells) > 6 else "",
                    "地市": cells[7] if len(cells) > 7 else "",
                    "商务": cells[9] if len(cells) > 9 else "",
                    "备注": cells[-1] if cells else "",
                })

print(f"文档 2 匹配到 {len(doc2_zones)} 条数据")

# 合并数据
all_zones = doc1_zones + doc2_zones
print(f"\n合并后总计：{len(all_zones)} 条数据")

# 去重
seen = set()
unique_zones = []
for zone in all_zones:
    key = zone.get("专区名称", "") + "|" + zone.get("分公司", "")
    if key not in seen and key.strip('|'):
        seen.add(key)
        unique_zones.append(zone)

print(f"去重后：{len(unique_zones)} 条数据")

# 统计
print("\n按大区统计:")
print("-" * 40)
region_count = {}
for zone in unique_zones:
    region = zone.get("大区", "未知")
    region_count[region] = region_count.get(region, 0) + 1

for region, count in sorted(region_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{region}: {count} 个")

# 保存 Excel
df = pd.DataFrame(unique_zones)
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_完整版.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 100)
print("陈海勇负责专区明细（前 50 条）")
print("=" * 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.head(50).to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_统计汇总.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("陈海勇负责专区统计汇总\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"总计：{len(df)} 个专区\n\n")
    f.write("按大区统计:\n")
    for region, count in sorted(region_count.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  {region}: {count} 个\n")

print(f"\n✅ 统计汇总已保存：{stats_file}")
