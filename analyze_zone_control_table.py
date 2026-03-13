# -*- coding: utf-8 -*-
"""
从专区管控表分析陈海勇负责的 12 个省份的专区
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

# 解析"专区推进（每周更新）"表格
lines = content_text.split('\n')
zones = []
in_zone_push_table = False

for line in lines:
    line = line.strip()
    if not line or not line.startswith('|'):
        continue
    
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    # 检测"专区推进（每周更新）"表格开始
    if '专区推进' in line or '每周更新' in line:
        in_zone_push_table = True
        continue
    
    # 检测"25 年新开专区"表格开始（结束上一个表格）
    if '25 年新开专区' in line:
        in_zone_push_table = False
        continue
    
    if not in_zone_push_table:
        continue
    
    # 跳过表头
    if len(cells) > 0 and '序号' in cells[0]:
        continue
    
    # 检测表格结束
    if len(cells) > 0 and cells[0] in ['注', '----', '☆']:
        continue
    
    # 需要足够多的列（至少 10 列）
    if len(cells) < 10:
        continue
    
    # 检查序号是否是数字
    if not cells[0].isdigit():
        continue
    
    # 获取省份信息（从分公司或备注中提取）
    province = ""
    分公司 = cells[4] if len(cells) > 4 else ""
    
    # 从分公司名称中提取省份
    if '沈阳' in 分公司 or '辽宁' in 分公司:
        province = "辽宁省"
    elif '郑州' in 分公司 or '河南' in 分公司:
        province = "河南省"
    elif '石家庄' in 分公司 or '河北' in 分公司:
        province = "河北省"
    elif '山东' in 分公司 or '济南' in 分公司:
        province = "山东省"
    elif '内蒙古' in 分公司 or '呼和浩特' in 分公司:
        province = "内蒙古"
    elif '新疆' in 分公司 or '乌鲁木齐' in 分公司:
        province = "新疆"
    elif '吉林' in 分公司 or '长春' in 分公司:
        province = "吉林省"
    elif '黑龙江' in 分公司 or '哈尔滨' in 分公司:
        province = "黑龙江省"
    elif '北京' in 分公司:
        province = "北京"
    elif '天津' in 分公司:
        province = "天津"
    elif '山西' in 分公司 or '太原' in 分公司:
        province = "山西"
    elif '湖北' in 分公司 or '武汉' in 分公司:
        province = "湖北省"
    
    # 检查是否属于陈海勇负责的省份
    if province:
        zone_info = {
            "序号": cells[0],
            "专区名称": cells[1] if len(cells) > 1 else "",
            "BU 侧集成运营": cells[2] if len(cells) > 2 else "",
            "里程碑节点": cells[3] if len(cells) > 3 else "",
            "最新进展": cells[4] if len(cells) > 4 else "",
            "是否今年新开": cells[5] if len(cells) > 5 else "",
            "备注": cells[6] if len(cells) > 6 else "",
            "是否上线": cells[7] if len(cells) > 7 else "",
            "今年是否产生收益": cells[8] if len(cells) > 8 else "",
            "收益 (万元)": cells[9] if len(cells) > 9 else "",
            "省份": province,
        }
        zones.append(zone_info)

print("Matched %d zones from Zone Control Table" % len(zones))

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
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_专区管控表分析.xlsx")
df.to_excel(output_file, index=False)

print("\n[OK] Excel saved to: %s" % output_file)
print("   Total: %d records" % len(df))

# 打印预览
print("\n" + "=" * 120)
print("Chen Haiyong's Zones (from Zone Control Table)")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 30)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_管控表分析_统计.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("Chen Haiyong Zones Summary (from Zone Control Table)\n")
    f.write("=" * 60 + "\n\n")
    f.write("Total: %d zones\n\n" % len(df))
    f.write("By Province:\n")
    for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
        f.write("  %s: %d\n" % (province, count))

print("\n[OK] Summary saved to: %s" % stats_file)
