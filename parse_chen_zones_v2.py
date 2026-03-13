# -*- coding: utf-8 -*-
"""
解析陈海勇负责的 12 个省份的专区 - 从腾讯文档数据
"""
import pandas as pd
import json
from pathlib import Path

# 陈海勇负责的 12 个省份关键词
chen_provinces = [
    "内蒙古", "辽宁", "吉林", "黑龙江",  # 华北区
    "河北", "湖北", "河南",  # 华中区
    "新疆",  # 西北区
    "北京", "天津",  # 政务华东区
    "山东",  # 交易华东区
    "山西"  # 补充
]

# 读取文档内容（JSON 格式）
doc_file = Path("D:/openclaw-workspace/output/doc2_sheet2.txt")
with open(doc_file, "r", encoding="utf-8") as f:
    content = f.read()

# 解析 JSON
try:
    data = json.loads(content)
    content_text = data.get("content", "")
except:
    content_text = content

# 解析表格行
lines = content_text.split('\n')
zones = []
in_25_new_table = False
headers = []

for line in lines:
    line = line.strip()
    if not line or not line.startswith('|'):
        continue
    
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    # 检测"25 年新开专区"表格开始
    if '25 年新开专区' in line:
        in_25_new_table = True
        continue
    
    if not in_25_new_table:
        continue
    
    # 检测表格结束
    if len(cells) > 0 and cells[0] in ['注', '----', '序号']:
        if '序号' in cells[0]:
            headers = cells
        continue
    
    # 需要足够多的列
    if len(cells) < 7:
        continue
    
    # 检查序号是否是数字
    if not cells[0].isdigit():
        continue
    
    # 获取省份（第 7 列，索引 6）
    province = cells[6] if len(cells) > 6 else ""
    
    # 检查是否属于陈海勇负责的省份
    matched_province = None
    for p in chen_provinces:
        if p in province:
            matched_province = p
            break
    
    if matched_province:
        zone_info = {
            "序号": cells[0],
            "专区名称": cells[1] if len(cells) > 1 else "",
            "客户名称": cells[2] if len(cells) > 2 else "",
            "系统版本": cells[3] if len(cells) > 3 else "",
            "分公司": cells[4] if len(cells) > 4 else "",
            "所属区域": cells[5] if len(cells) > 5 else "",
            "省份": province,
            "地市": cells[7] if len(cells) > 7 else "",
            "BU 侧集成运营": cells[8] if len(cells) > 8 else "",
            "商务": cells[9] if len(cells) > 9 else "",
            "交付": cells[10] if len(cells) > 10 else "",
            "接入日期": cells[11] if len(cells) > 11 else "",
        }
        zones.append(zone_info)

print("Matched %d zones" % len(zones))

# 按省份统计
print("\nBy Province:")
print("-" * 40)
province_count = {}
for zone in zones:
    province = zone.get("省份", "Unknown")
    province_count[province] = province_count.get(province, 0) + 1

for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
    print("%s: %d" % (province, count))

# 保存 Excel
df = pd.DataFrame(zones)
output_file = Path("D:/openclaw-workspace/output/chen_haiyong_zones_12provinces.xlsx")
df.to_excel(output_file, index=False)

print("\n[OK] Excel saved to: %s" % output_file)
print("   Total: %d records" % len(df))

# 打印预览
print("\n" + "=" * 120)
print("Chen Haiyong's Zones (25 New, 12 Provinces)")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/chen_haiyong_zones_summary.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("Chen Haiyong Zones Summary (25 New, 12 Provinces)\n")
    f.write("=" * 60 + "\n\n")
    f.write("Total: %d zones\n\n" % len(df))
    f.write("By Province:\n")
    for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
        f.write("  %s: %d\n" % (province, count))
    f.write("\nProvince List:\n")
    for p in chen_provinces:
        f.write("  - %s\n" % p)

print("\n[OK] Summary saved to: %s" % stats_file)
