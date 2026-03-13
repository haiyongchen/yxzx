# -*- coding: utf-8 -*-
"""
陈海勇负责专区统计 - 12 个指定省份
根据架构图，陈海勇负责的区域：
- 华北区：内蒙古、辽宁、吉林、黑龙江
- 华中区：河北、湖北、河南
- 西北区：新疆
- 政务华东区：北京、天津
- 交易华东区：山东
- 补充：山西
"""
import pandas as pd
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

def is_chen_province(text):
    """检查是否属于陈海勇负责的省份"""
    if not text:
        return False
    for province in chen_provinces:
        if province in text:
            return True
    return False

# 读取文档 2（25 年新开专区）
doc2_file = Path("D:/openclaw-workspace/output/doc2_sheet2.txt")
with open(doc2_file, "r", encoding="utf-8") as f:
    doc2_content = f.read()

# 解析"25 年新开专区"表格
print("=" * 80)
print("解析文档 2:25 年新开专区表格")
print("=" * 80)

doc2_lines = doc2_content.split('\n')
zones_2025 = []
in_25_new_table = False
header_found = False

for line in doc2_lines:
    # 检测表格开始
    if '|25 年新开专区' in line:
        in_25_new_table = True
        continue
    
    if not in_25_new_table:
        continue
    
    # 检测表格结束（下一个表格开始）
    if line.strip().startswith('|') and any(x in line for x in ['待接入专区', '公告对接', '湖北地区', '已上线未', '收费标准', '专区管控', '落地部署', '暂保留', '增量部分', '新开专区上量', '低收益', '专区推进', '无量专区']):
        in_25_new_table = False
        continue
    
    if '|' not in line or len(line) < 50:
        continue
    
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    # 跳过表头
    if len(cells) > 0 and cells[0] in ['序号', '注', '序号', '专区名称']:
        header_found = True
        continue
    
    if not header_found:
        continue
    
    # 需要至少有序号列和省份列
    if len(cells) < 7:
        continue
    
    # 检查序号是否是数字
    if not cells[0].isdigit():
        continue
    
    # 获取省份（第 7 列，索引 6）
    province = cells[6] if len(cells) > 6 else ""
    
    # 检查是否属于陈海勇负责的省份
    if is_chen_province(province):
        zone_info = {
            "来源": "文档 2-25 年新开专区",
            "序号": cells[0],
            "专区名称": cells[1] if len(cells) > 1 else "",
            "客户名称": cells[2] if len(cells) > 2 else "",
            "系统版本": cells[3] if len(cells) > 3 else "",
            "分公司": cells[4] if len(cells) > 4 else "",
            "所属": cells[5] if len(cells) > 5 else "",
            "省份": province,
            "地市": cells[7] if len(cells) > 7 else "",
            "BU 侧集成运营": cells[8] if len(cells) > 8 else "",
            "商务": cells[9] if len(cells) > 9 else "",
            "交付": cells[10] if len(cells) > 10 else "",
            "接入日期": cells[11] if len(cells) > 11 else "",
            "备注": cells[-1] if cells else "",
        }
        zones_2025.append(zone_info)

print(f"25 年新开专区匹配到 {len(zones_2025)} 条数据")

# 按省份统计
print("\n按省份统计:")
print("-" * 40)
province_count = {}
for zone in zones_2025:
    province = zone.get("省份", "未知")
    province_count[province] = province_count.get(province, 0) + 1

for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{province}: {count} 个")

# 保存 Excel
df = pd.DataFrame(zones_2025)
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_25 年新开_12 省份.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 120)
print("陈海勇负责专区明细（25 年新开，12 省份）")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 15)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_25 年新开_统计.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("陈海勇负责专区统计汇总（25 年新开，12 省份）\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"总计：{len(df)} 个专区\n\n")
    f.write("按省份统计:\n")
    for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  {province}: {count} 个\n")
    f.write("\n指定省份列表:\n")
    for p in chen_provinces:
        f.write(f"  - {p}\n")

print(f"\n✅ 统计汇总已保存：{stats_file}")
