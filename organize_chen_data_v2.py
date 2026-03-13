# -*- coding: utf-8 -*-
"""
根据架构图整理陈海勇负责的专区信息
"""
import pandas as pd
import json
import re
from pathlib import Path

# 陈海勇负责的分公司列表（根据架构图）
chen_haiyong_regions = {
    "华北区": [
        "交易呼和浩特分公司",
        "交易沈阳分公司", 
        "数字采购沈阳分公司",
        "交易长春分公司",
        "交付服务部"
    ],
    "华中区": [
        "石家庄分公司",
        "交易武汉分公司",
        "交易郑州分公司",
        "交易交付服务部"
    ],
    "西北区": [
        "交易乌鲁木齐分公司",
        "交易兵团分公司",
        "交易交付服务部"
    ],
    "政务华东区": [
        "交易北京分公司",
        "交付服务部"
    ],
    "交易华东区": [
        "交易济南分公司"
    ]
}

# 展平所有分公司
chen_branches = []
for region, branches in chen_haiyong_regions.items():
    for branch in branches:
        chen_branches.append({
            "大区": region,
            "分公司": branch
        })

print("陈海勇负责的分公司:")
for item in chen_branches:
    print(f"  {item['大区']}: {item['分公司']}")

# 第一个文档的列头（01-新点电子交易专区&项目跟进表）
doc1_columns = [
    "专区码", "专区名称", "客户类型", "分公司", "省份", "地市", 
    "所属平台", "项目经理", "远程交付", "商务", "开发", 
    "确认接入时间", "专区上线自检表反馈时间", "专区状态",
    "是否开设智能助手", "接入申请邮件地址", "标识"
]

# 读取第一个文档内容（已获取的 JSON 数据）
doc1_content = """|专区管控表
||专区码|     | 专区名称 | 客户类型 | 分公司 | 省份 | 地市 | 所属平台 | 项目经理 | 远程交付 | 商务 | 开发 | 确认接入时间 | 专区上线自检表反馈时间 | 专区状态 | 是否开设智能助手 | 接入申请邮件地址 | 标识 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|C2021010146|DQ_HuaSha|华厦专区||企业 | 交易云服务华东分公司 | 江苏省 | 南京市 | 新点电子交易平台（7.0）||张家希 | 杨涛（交易云服务华东分公司）|张渝、陈章|2018/7/1|2019/9/1|上线有量|||无 |
|C2022040002|DQ_XuanCheng|宣城专区||政府 | 交易云服务华南分公司 | 安徽省 | 宣城市 | 新点电子交易平台（7.0）|姚建洋 | 张园园 | 陈伟 | 王寅迟、陈强|2018/8/1|2018/9/24|上线有量||||
|C2021010137|DQ_DongHai|东海专区||企业 | 交易云服务华东分公司 | 江苏省 | 连云港市 | 江苏限额以下平台（7.0）|张海南 | 顾梦娇 | 杨涛（交易云服务华东分公司）|张渝、陈章|2018/8/1|2018/9/1|上线有量||||
"""

# 解析文档内容
def parse_table_content(content):
    """解析表格内容"""
    rows = []
    lines = content.strip().split('\n')
    
    for line in lines[3:]:  # 跳过表头
        if line.startswith('|C') or line.startswith('||'):
            cells = line.split('|')
            cells = [c.strip() for c in cells if c.strip()]
            if len(cells) >= 5:
                rows.append(cells)
    
    return rows

# 测试解析
test_rows = parse_table_content(doc1_content)
print(f"\n解析到 {len(test_rows)} 行数据")

# 匹配陈海勇负责的分公司
def match_chen_branches(rows, chen_branches):
    """匹配陈海勇负责的分公司"""
    matched = []
    
    for row in rows:
        # 假设分公司在第 5 列（索引 4）
        if len(row) > 4:
            branch = row[4] if len(row) > 4 else ""
            
            # 检查是否匹配陈海勇负责的分公司
            for chen_branch in chen_branches:
                if chen_branch['分公司'] in branch or branch in chen_branch['分公司']:
                    matched.append({
                        "大区": chen_branch['大区'],
                        "数据": row
                    })
                    break
    
    return matched

# 测试匹配
matched_data = match_chen_branches(test_rows, chen_branches)
print(f"匹配到 {len(matched_data)} 条陈海勇负责的数据")

print("\n✅ 脚本准备完成，等待完整数据后生成 Excel")
