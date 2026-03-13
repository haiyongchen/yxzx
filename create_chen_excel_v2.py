# -*- coding: utf-8 -*-
"""
生成陈海勇负责的所有专区明细 Excel
"""
import pandas as pd
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

# 创建 DataFrame
data_for_df = []
for item in matched_zones:
    row_data = item["数据"]
    
    # 提取关键信息
    zone_info = {
        "大区": item["大区"],
        "匹配城市": item["匹配关键词"],
        "专区码": row_data[1] if len(row_data) > 1 else "",
        "专区名称": row_data[2] if len(row_data) > 2 else "",
        "客户类型": row_data[3] if len(row_data) > 3 else "",
        "分公司": row_data[4] if len(row_data) > 4 else "",
        "省份": row_data[5] if len(row_data) > 5 else "",
        "地市": row_data[6] if len(row_data) > 6 else "",
        "所属平台": row_data[7] if len(row_data) > 7 else "",
        "项目经理": row_data[8] if len(row_data) > 8 else "",
        "远程交付": row_data[9] if len(row_data) > 9 else "",
        "商务": row_data[10] if len(row_data) > 10 else "",
        "开发": row_data[11] if len(row_data) > 11 else "",
        "确认接入时间": row_data[12] if len(row_data) > 12 else "",
        "专区状态": row_data[14] if len(row_data) > 14 else "",
    }
    data_for_df.append(zone_info)

df = pd.DataFrame(data_for_df)

# 保存为 Excel
output_file = Path("D:/openclaw-workspace/output/陈海勇负责专区明细_完整版.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Excel 已生成：{output_file}")
print(f"   共 {len(df)} 条记录")

# 按大区统计
print("\n按大区统计:")
summary = df.groupby("大区").size().reset_index(name="专区数量")
print(summary.to_string(index=False))

# 打印预览
print("\n" + "=" * 100)
print("陈海勇负责专区明细（前 30 条）")
print("=" * 100)
print(df.to_string(index=False, max_rows=30))
