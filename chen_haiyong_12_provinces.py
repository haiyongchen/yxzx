# -*- coding: utf-8 -*-
"""
陈海勇负责专区统计 - 只统计指定 12 个省份
根据架构图，陈海勇负责的区域：
- 华北区：内蒙古、辽宁、吉林、黑龙江、北京、天津
- 华中区：河北、湖北、河南
- 西北区：新疆
- 交易华东区：山东
- 政务华东区：北京、天津
"""
import pandas as pd
from pathlib import Path

# 陈海勇负责的 12 个省份
chen_provinces = [
    "内蒙古", "辽宁", "吉林", "黑龙江",  # 华北区
    "北京", "天津",  # 政务华东区
    "山东",  # 交易华东区
    "河北", "湖北", "河南",  # 华中区
    "新疆",  # 西北区
    "山西"  # 补充
]

def is_chen_province(text):
    """检查是否属于陈海勇负责的省份"""
    if not text:
        return False
    for province in chen_provinces:
        if province in text:
            return True
    return False

# 读取文档 1（专区管控表）
doc1_file = Path("D:/openclaw-workspace/output/doc1_sheet1.txt")
with open(doc1_file, "r", encoding="utf-8") as f:
    doc1_content = f.read()

# 读取文档 2（25 年新开专区）
doc2_file = Path("D:/openclaw-workspace/output/doc2_sheet2.txt")
with open(doc2_file, "r", encoding="utf-8") as f:
    doc2_content = f.read()

# 解析文档 1
print("=" * 80)
print("解析文档 1：专区管控表")
print("=" * 80)

doc1_lines = doc1_content.split('\n')
doc1_zones = []

for line in doc1_lines:
    if '|' in line and len(line) > 50:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 10:
            row_text = ' | '.join(cells)
            
            # 检查省份
            province = cells[5] if len(cells) > 5 else ""
            
            if is_chen_province(province) and '分公司' not in cells[0] and '#ERROR!' not in cells[0]:
                doc1_zones.append({
                    "来源": "文档 1-专区管控表",
                    "专区码": cells[1] if len(cells) > 1 else "",
                    "专区名称": cells[2] if len(cells) > 2 else "",
                    "客户类型": cells[3] if len(cells) > 3 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": province,
                    "地市": cells[6] if len(cells) > 6 else "",
                    "所属平台": cells[7] if len(cells) > 7 else "",
                    "项目经理": cells[8] if len(cells) > 8 else "",
                    "远程交付": cells[9] if len(cells) > 9 else "",
                    "商务": cells[10] if len(cells) > 10 else "",
                    "开发": cells[11] if len(cells) > 11 else "",
                    "确认接入时间": cells[12] if len(cells) > 12 else "",
                    "专区状态": cells[14] if len(cells) > 14 else "",
                })

print(f"文档 1 匹配到 {len(doc1_zones)} 条数据")

# 解析文档 2（25 年新开专区）
print("\n解析文档 2:25 年新开专区")
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
        if len(cells) > 0 and cells[0] in ['序号', '注', '专区推进', '低收益', '增量', '无量', '新开', '落地']:
            if cells[0] == '序号':
                continue
            else:
                in_25_new_table = False
                continue
        
        if len(cells) >= 7:
            # 检查省份（第 7 列）
            province = cells[6] if len(cells) > 6 else ""
            
            # 检查是否是数据行（序号是数字）
            if is_chen_province(province) and len(cells) > 0 and cells[0].isdigit():
                doc2_zones.append({
                    "来源": "文档 2-25 年新开专区",
                    "专区名称": cells[1] if len(cells) > 1 else "",
                    "客户名称": cells[2] if len(cells) > 2 else "",
                    "系统版本": cells[3] if len(cells) > 3 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": province,
                    "地市": cells[7] if len(cells) > 7 else "",
                    "BU 侧集成运营": cells[8] if len(cells) > 8 else "",
                    "商务": cells[9] if len(cells) > 9 else "",
                    "交付": cells[10] if len(cells) > 10 else "",
                    "接入日期": cells[11] if len(cells) > 11 else "",
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
    key = zone.get("专区名称", "") + "|" + zone.get("分公司", "") + "|" + zone.get("省份", "")
    if key not in seen and key.strip('|'):
        seen.add(key)
        unique_zones.append(zone)

print(f"去重后：{len(unique_zones)} 条数据")

# 按省份统计
print("\n按省份统计:")
print("-" * 40)
province_count = {}
for zone in unique_zones:
    province = zone.get("省份", "未知")
    province_count[province] = province_count.get(province, 0) + 1

for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{province}: {count} 个")

# 保存 Excel
df = pd.DataFrame(unique_zones)
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_12 省份完整版.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 120)
print("陈海勇负责专区明细（全部）")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 15)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_12 省份统计.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("陈海勇负责专区统计汇总（12 省份）\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"总计：{len(df)} 个专区\n\n")
    f.write("按省份统计:\n")
    for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  {province}: {count} 个\n")
    f.write("\n指定省份列表:\n")
    for p in chen_provinces:
        f.write(f"  - {p}\n")

print(f"\n✅ 统计汇总已保存：{stats_file}")
