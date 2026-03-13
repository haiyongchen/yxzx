# -*- coding: utf-8 -*-
"""
使用腾讯文档技能获取完整专区数据
"""
import subprocess
import json
import re
from pathlib import Path

# 陈海勇负责的分公司关键词
chen_branches = [
    "呼和浩特", "沈阳", "长春", "石家庄", "武汉", "郑州", 
    "乌鲁木齐", "北京", "天津", "济南"
]

def get_doc_content(file_id):
    """获取腾讯文档内容"""
    cmd = f'mcporter call tencent-docs.get_content file_id:{file_id}'
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, 'TENCENT_DOCS_TOKEN': 'e23255dcdf51491cb208ecc9cc341e21'}
        )
        return result.stdout
    except Exception as e:
        print(f"获取文档失败：{e}")
        return None

def parse_table_rows(content):
    """解析表格行"""
    rows = []
    lines = content.split('\n')
    
    for line in lines:
        if '|' in line and len(line) > 20:
            # 提取表格单元格
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) >= 5:
                rows.append(cells)
    
    return rows

def match_chen_branches(rows):
    """匹配陈海勇负责的分公司"""
    matched = []
    
    for row in rows:
        # 查找分公司列（通常在第 4-6 列）
        for i, cell in enumerate(row):
            for branch in chen_branches:
                if branch in cell:
                    matched.append({
                        '分公司': cell,
                        '行数据': row,
                        '匹配关键词': branch
                    })
                    break
    
    return matched

# 获取文档 1 内容
print("正在获取文档 1 内容...")
doc1_content = get_doc_content("DTFdkY3NqamJJVEJl")

if doc1_content:
    # 保存原始内容
    output_file = Path("D:/openclaw-workspace/output/doc1_full.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(doc1_content)
    print(f"文档 1 内容已保存：{output_file}")
    
    # 解析表格
    rows = parse_table_rows(doc1_content)
    print(f"解析到 {len(rows)} 行表格数据")
    
    # 匹配陈海勇负责的分公司
    matched = match_chen_branches(rows)
    print(f"匹配到 {len(matched)} 条陈海勇负责的数据")
    
    # 保存匹配结果
    if matched:
        matched_file = Path("D:/openclaw-workspace/output/chen_branches_matched.txt")
        with open(matched_file, "w", encoding="utf-8") as f:
            for item in matched:
                f.write(f"匹配关键词：{item['匹配关键词']}\n")
                f.write(f"分公司：{item['分公司']}\n")
                f.write(f"完整数据：{' | '.join(item['行数据'][:10])}\n")
                f.write("-" * 80 + "\n")
        print(f"匹配结果已保存：{matched_file}")
else:
    print("❌ 无法获取文档内容")

print("\n完成")
