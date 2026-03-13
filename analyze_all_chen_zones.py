# -*- coding: utf-8 -*-
"""
从腾讯文档完整分析陈海勇负责的 12 个省份的专区
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

# 分公司到省份的映射
branch_to_province = {
    "沈阳分公司": "辽宁省",
    "郑州分公司": "河南省",
    "石家庄分公司": "河北省",
    "武汉分公司": "湖北省",
    "华北分公司": "内蒙古",
    "华东分公司": "山东省",
    "交易云服务华东分公司": "山东省",
    "交易云服务华北分公司": "内蒙古",
}

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

# 存储所有专区数据
all_zones = []
in_25_new_table = False

for line in lines:
    line = line.strip()
    if not line or not line.startswith('|'):
        continue
    
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    # 检测"25 年新开专区"表格开始
    if '25 年新开专区' in line:
        in_25_new_table = True
        continue
    
    # 检测表格结束
    if len(cells) > 0 and cells[0] in ['注', '----']:
        continue
    
    # 跳过表头
    if len(cells) > 0 and '序号' in cells[0]:
        continue
    
    # 需要足够多的列（至少 7 列）
    if len(cells) < 7:
        continue
    
    # 检查序号是否是数字
    if not cells[0].isdigit():
        continue
    
    # 获取省份（第 7 列，索引 6）
    province = cells[6] if len(cells) > 6 else ""
    
    # 检查是否属于陈海勇负责的省份
    is_chen_province = False
    for p in chen_provinces:
        if p in province:
            is_chen_province = True
            break
    
    if is_chen_province:
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
            "来源表格": "25 年新开专区",
        }
        all_zones.append(zone_info)

print("Matched %d zones from 25 New Zones table" % len(all_zones))

# 按省份统计
print("\nBy Province:")
print("-" * 40)
province_count = {}
for zone in all_zones:
    province = zone.get("省份", "Unknown")
    province_count[province] = province_count.get(province, 0) + 1

for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
    print("%s: %d" % (province, count))

# 保存 Excel
df = pd.DataFrame(all_zones)
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_完整分析.xlsx")
df.to_excel(output_file, index=False)

print("\n[OK] Excel saved to: %s" % output_file)
print("   Total: %d records" % len(df))

# 打印预览
print("\n" + "=" * 150)
print("Chen Haiyong's Zones - Complete Analysis")
print("=" * 150)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 30)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_完整分析_统计.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("Chen Haiyong Zones Summary - Complete Analysis\n")
    f.write("=" * 60 + "\n\n")
    f.write("Total: %d zones\n\n" % len(df))
    f.write("By Province:\n")
    for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
        f.write("  %s: %d\n" % (province, count))

print("\n[OK] Summary saved to: %s" % stats_file)
