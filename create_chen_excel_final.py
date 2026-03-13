# -*- coding: utf-8 -*-
"""
根据架构图整理陈海勇负责的所有专区明细
结合两个腾讯文档的数据，按分公司/省份精确匹配
"""
import pandas as pd
import re
from pathlib import Path

# 陈海勇负责的区域映射（根据架构图）
chen_regions = {
    "华北区": {
        "分公司关键词": ["呼和浩特", "沈阳", "长春", "华北"],
        "省份关键词": ["内蒙古", "辽宁", "吉林", "黑龙江"],
        "城市关键词": ["呼和浩特", "沈阳", "长春", "哈尔滨"]
    },
    "华中区": {
        "分公司关键词": ["石家庄", "武汉", "郑州", "华中"],
        "省份关键词": ["河北", "湖北", "河南"],
        "城市关键词": ["石家庄", "武汉", "郑州"]
    },
    "西北区": {
        "分公司关键词": ["乌鲁木齐", "西北"],
        "省份关键词": ["新疆", "甘肃", "青海", "宁夏", "陕西"],
        "城市关键词": ["乌鲁木齐"]
    },
    "政务华东区": {
        "分公司关键词": ["北京", "天津", "政务"],
        "省份关键词": ["北京", "天津"],
        "城市关键词": ["北京", "天津"]
    },
    "交易华东区": {
        "分公司关键词": ["济南", "华东"],
        "省份关键词": ["山东"],
        "城市关键词": ["济南", "青岛", "烟台"]
    }
}

def match_chen_region(row_text):
    """匹配陈海勇负责的大区"""
    for region, keywords in chen_regions.items():
        # 检查分公司关键词
        for kw in keywords["分公司关键词"]:
            if kw in row_text:
                return region, f"分公司:{kw}"
        
        # 检查省份关键词
        for kw in keywords["省份关键词"]:
            if kw in row_text:
                return region, f"省份:{kw}"
        
        # 检查城市关键词
        for kw in keywords["城市关键词"]:
            if kw in row_text:
                return region, f"城市:{kw}"
    
    return None, None

# 读取文档 1 内容（专区管控表）
doc1_file = Path("D:/openclaw-workspace/output/doc1_content.txt")
with open(doc1_file, "r", encoding="utf-8") as f:
    doc1_content = f.read()

# 读取文档 2 内容（上量信息统计）
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
        if len(cells) >= 10 and '专区' in line:
            row_text = ' | '.join(cells)
            region, match_type = match_chen_region(row_text)
            
            if region:
                zone_info = {
                    "来源": "文档 1-专区管控表",
                    "大区": region,
                    "匹配类型": match_type,
                    "专区码": cells[1] if len(cells) > 1 else "",
                    "专区名称": cells[2] if len(cells) > 2 else "",
                    "客户类型": cells[3] if len(cells) > 3 else "",
                    "分公司": cells[4] if len(cells) > 4 else "",
                    "省份": cells[5] if len(cells) > 5 else "",
                    "地市": cells[6] if len(cells) > 6 else "",
                    "所属平台": cells[7] if len(cells) > 7 else "",
                    "项目经理": cells[8] if len(cells) > 8 else "",
                    "远程交付": cells[9] if len(cells) > 9 else "",
                    "商务": cells[10] if len(cells) > 10 else "",
                    "开发": cells[11] if len(cells) > 11 else "",
                    "确认接入时间": cells[12] if len(cells) > 12 else "",
                    "专区状态": cells[14] if len(cells) > 14 else "",
                }
                doc1_zones.append(zone_info)

print(f"文档 1 匹配到 {len(doc1_zones)} 条陈海勇负责的专区数据")

# 解析文档 2（上量信息统计）
print("\n解析文档 2：专区上量信息统计表")
print("=" * 80)

doc2_lines = doc2_content.split('\n')
doc2_zones = []

for line in doc2_lines:
    if '|' in line and len(line) > 50:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 5 and ('专区' in line or '分公司' in line):
            row_text = ' | '.join(cells)
            region, match_type = match_chen_region(row_text)
            
            if region:
                zone_info = {
                    "来源": "文档 2-上量信息统计",
                    "大区": region,
                    "匹配类型": match_type,
                    "专区名称": cells[0] if len(cells) > 0 else "",
                    "系统版本": cells[1] if len(cells) > 1 else "",
                    "分公司": cells[2] if len(cells) > 2 else "",
                    "省份": cells[3] if len(cells) > 3 else "",
                    "地市": cells[4] if len(cells) > 4 else "",
                    "BU 侧集成运营": cells[5] if len(cells) > 5 else "",
                    "商务": cells[6] if len(cells) > 6 else "",
                    "备注": cells[-1] if cells else "",
                }
                doc2_zones.append(zone_info)

print(f"文档 2 匹配到 {len(doc2_zones)} 条陈海勇负责的专区数据")

# 合并数据
all_zones = doc1_zones + doc2_zones

# 去重（按专区名称）
seen = set()
unique_zones = []
for zone in all_zones:
    zone_key = zone.get("专区名称", "") + zone.get("专区码", "")
    if zone_key not in seen and zone_key:
        seen.add(zone_key)
        unique_zones.append(zone)

print(f"\n去重后总计：{len(unique_zones)} 条陈海勇负责的专区数据")

# 按大区统计
print("\n按大区统计:")
print("-" * 40)
region_count = {}
for zone in unique_zones:
    region = zone.get("大区", "未知")
    region_count[region] = region_count.get(region, 0) + 1

for region, count in sorted(region_count.items()):
    print(f"{region}: {count} 个专区")

# 创建 DataFrame 并保存 Excel
df = pd.DataFrame(unique_zones)

# 重新排序列
if "文档 1" in df["来源"].values:
    cols_order = ["来源", "大区", "匹配类型", "专区码", "专区名称", "客户类型", "分公司", "省份", "地市", "所属平台", "项目经理", "远程交付", "商务", "开发", "确认接入时间", "专区状态"]
else:
    cols_order = ["来源", "大区", "匹配类型", "专区名称", "系统版本", "分公司", "省份", "地市", "BU 侧集成运营", "商务", "备注"]

# 只保留存在的列
available_cols = [c for c in cols_order if c in df.columns]
df = df[available_cols]

# 保存 Excel
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_完整版_v2.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 100)
print("陈海勇负责专区明细（前 50 条）")
print("=" * 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)
print(df.head(50).to_string(index=False))

# 保存为 CSV（方便查看）
csv_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_完整版.csv")
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"\n✅ CSV 已生成：{csv_file}")
