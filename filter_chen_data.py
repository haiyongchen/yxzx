# -*- coding: utf-8 -*-
"""
从腾讯文档数据中筛选陈海勇负责的专区
"""
import pandas as pd
import json
import re
from pathlib import Path

# 陈海勇负责的分公司关键词
chen_keywords = [
    "呼和浩特", "沈阳", "长春", "石家庄", "武汉", "郑州", 
    "乌鲁木齐", "北京", "天津", "济南"
]

# 读取第一个文档内容（专区管控表）
doc1_file = Path("D:/openclaw-workspace/output/doc1_content.txt")

if doc1_file.exists():
    with open(doc1_file, "r", encoding="utf-8") as f:
        doc1_content = f.read()
    
    # 解析表格行
    lines = doc1_content.strip().split('\n')
    
    matched_rows = []
    for line in lines:
        # 检查是否包含陈海勇负责的分公司关键词
        for keyword in chen_keywords:
            if keyword in line:
                matched_rows.append(line)
                break
    
    print(f"从文档 1 中匹配到 {len(matched_rows)} 条相关数据")
    
    # 保存匹配结果
    output_file = Path("D:/openclaw-workspace/output/chen_matched_rows.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('\n'.join(matched_rows))
    
    print(f"匹配结果已保存：{output_file}")
    
    # 打印预览
    print("\n匹配数据预览:")
    for i, row in enumerate(matched_rows[:10]):
        print(f"{i+1}. {row[:150]}...")
else:
    print("❌ 未找到文档内容文件")

print("\n✅ 完成")
