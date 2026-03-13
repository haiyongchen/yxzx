# -*- coding: utf-8 -*-
"""
解析陈海勇负责的 12 个省份的专区
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

# 读取文档内容
doc_file = Path("D:/openclaw-workspace/output/doc2_full.txt")
with open(doc_file, "r", encoding="utf-8") as f:
    content = f.read()

# 解析表格行
lines = content.split('\n')
zones = []
in_table = False
headers = []

for line in lines:
    line = line.strip()
    if not line or not line.startswith('|'):
        continue
    
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    # 检测表头
    if len(cells) > 0 and '序号' in cells[0]:
        headers = cells
        in_table = True
        continue
    
    if not in_table:
        continue
    
    # 检测表格结束
    if len(cells) > 0 and cells[0] in ['注', '----']:
        in_table = False
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

print(f"匹配到 {len(zones)} 条陈海勇负责的专区数据")

# 按省份统计
print("\n按省份统计:")
print("-" * 40)
province_count = {}
for zone in zones:
    province = zone.get("省份", "未知")
    province_count[province] = province_count.get(province, 0) + 1

for province, count in sorted(province_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{province}: {count} 个")

# 保存 Excel
df = pd.DataFrame(zones)
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_25 年新开_12 省份_最终版.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 120)
print("陈海勇负责专区明细（25 年新开，12 省份）")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)
print(df.to_string(index=False))

# 保存统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_统计汇总.txt")
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
