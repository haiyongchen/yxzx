# -*- coding: utf-8 -*-
"""
根据架构图整理陈海勇负责的所有专区明细 - 最终优化版
结合两个腾讯文档的数据，按分公司/省份精确匹配
"""
import pandas as pd
from pathlib import Path

# 陈海勇负责的区域映射（根据架构图）- 更精确的关键词
chen_regions = {
    "华北区": {
        "分公司": ["呼和浩特", "沈阳", "长春", "华北分公司"],
        "省份": ["内蒙古", "辽宁", "吉林", "黑龙江"],
        "城市": ["呼和浩特", "沈阳", "长春", "哈尔滨", "大庆"]
    },
    "华中区": {
        "分公司": ["石家庄", "武汉", "郑州", "华中"],
        "省份": ["河北", "湖北", "河南"],
        "城市": ["石家庄", "武汉", "郑州", "洛阳", "开封"]
    },
    "西北区": {
        "分公司": ["乌鲁木齐", "西北", "西安"],
        "省份": ["新疆", "甘肃", "青海", "宁夏", "陕西"],
        "城市": ["乌鲁木齐", "兰州", "西宁", "银川", "西安"]
    },
    "政务华东区": {
        "分公司": ["北京", "天津"],
        "省份": ["北京", "天津"],
        "城市": ["北京", "天津"]
    },
    "交易华东区": {
        "分公司": ["济南", "华东分公司", "交易云服务华东"],
        "省份": ["山东"],
        "城市": ["济南", "青岛", "烟台", "威海", "潍坊"]
    }
}

def match_chen_region_v2(text):
    """优化版匹配逻辑"""
    if not text or text == "#ERROR!":
        return None, None
    
    for region, keywords in chen_regions.items():
        # 检查分公司
        for kw in keywords["分公司"]:
            if kw in text:
                return region, f"分公司:{kw}"
        
        # 检查省份
        for kw in keywords["省份"]:
            if kw in text:
                return region, f"省份:{kw}"
        
        # 检查城市
        for kw in keywords["城市"]:
            if kw in text:
                return region, f"城市:{kw}"
    
    return None, None

# 读取文档 1 内容
doc1_file = Path("D:/openclaw-workspace/output/doc1_content.txt")
with open(doc1_file, "r", encoding="utf-8") as f:
    doc1_content = f.read()

# 读取文档 2 内容
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
            # 检查是否是专区数据行
            row_text = ' | '.join(cells)
            
            # 跳过表头和统计行
            if '分公司' in cells[0] or '专区码' in cells[0] or '#ERROR!' in cells[0]:
                continue
            
            region, match_type = match_chen_region_v2(row_text)
            
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

# 解析文档 2（上量信息统计）- 专门处理不同表格
print("\n解析文档 2：专区上量信息统计表")
print("=" * 80)

doc2_lines = doc2_content.split('\n')
doc2_zones = []

# 标记当前解析的表格
current_table = None

for line in doc2_lines:
    if '|' in line and len(line) > 30:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        
        # 检测表格类型
        if '低收益专区业绩承诺' in line:
            current_table = "低收益"
            continue
        elif '增量部分专区上量' in line:
            current_table = "增量"
            continue
        elif '2025 年第一季度无量专区' in line:
            current_table = "无量"
            continue
        elif '新开专区上量' in line:
            current_table = "新开"
            continue
        elif '25 年新开专区' in line:
            current_table = "25 新开"
            continue
        elif '专区推进' in line:
            current_table = "推进"
            continue
        
        # 跳过表头
        if not current_table or len(cells) < 5:
            continue
        
        # 跳过纯表头行
        if '序号' in cells[0] or '专区名称' in cells[0] or '分公司' in cells[0]:
            continue
        
        row_text = ' | '.join(cells)
        
        # 匹配陈海勇负责的区域
        region, match_type = match_chen_region_v2(row_text)
        
        if region:
            zone_info = {
                "来源": f"文档 2-{current_table}",
                "大区": region,
                "匹配类型": match_type,
                "专区名称": cells[0] if len(cells) > 0 else "",
                "分公司": cells[2] if len(cells) > 2 else "",
                "省份": cells[3] if len(cells) > 3 else "",
                "地市": cells[4] if len(cells) > 4 else "",
                "备注": cells[-1] if cells else "",
            }
            doc2_zones.append(zone_info)

print(f"文档 2 匹配到 {len(doc2_zones)} 条陈海勇负责的专区数据")

# 合并数据
all_zones = doc1_zones + doc2_zones

# 去重（按专区名称 + 分公司）
seen = set()
unique_zones = []
for zone in all_zones:
    zone_key = zone.get("专区名称", "") + "|" + zone.get("分公司", "") + "|" + zone.get("省份", "")
    if zone_key not in seen and zone_key.strip('|'):
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

for region, count in sorted(region_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{region}: {count} 个专区")

# 创建 DataFrame 并保存
df = pd.DataFrame(unique_zones)

# 保存 Excel
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_最终版.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 打印预览
print("\n" + "=" * 120)
print("陈海勇负责专区明细（前 80 条）")
print("=" * 120)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 15)
print(df.head(80).to_string(index=False))

# 保存 CSV
csv_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_最终版.csv")
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"\n✅ CSV 已生成：{csv_file}")

# 保存详细统计
stats_file = Path("D:/openclaw-workspace/output/陈海勇负责专区_统计汇总.txt")
with open(stats_file, "w", encoding="utf-8") as f:
    f.write("陈海勇负责专区统计汇总\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"总计：{len(df)} 个专区\n\n")
    f.write("按大区统计:\n")
    for region, count in sorted(region_count.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  {region}: {count} 个\n")
    f.write("\n按来源统计:\n")
    source_count = df.groupby("来源").size().to_dict()
    for source, count in sorted(source_count.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  {source}: {count} 个\n")

print(f"\n✅ 统计汇总已保存：{stats_file}")
