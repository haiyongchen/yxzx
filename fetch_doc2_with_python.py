# -*- coding: utf-8 -*-
"""
使用腾讯文档技能获取文档内容
"""
import subprocess
import json
from pathlib import Path

# 设置环境变量
import os
os.environ['TENCENT_DOCS_TOKEN'] = "e23255dcdf51491cb208ecc9cc341e21"

# 调用腾讯文档技能
doc_id = "DQnZoWXpYQU5HVEpz"

# 使用 subprocess 调用 mcporter
cmd = ['mcporter', 'call', 'tencent-docs.get_content', '--args', json.dumps({"file_id": doc_id})]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    output_file = Path("D:/openclaw-workspace/output/doc2_full.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    
    # 统计行数
    lines = result.stdout.split('\n')
    print(f"获取到 {len(lines)} 行数据")
    print(f"已保存到：{output_file}")
    
    # 查找包含省份的行
    chen_provinces = ["内蒙古", "辽宁", "吉林", "黑龙江", "河北", "湖北", "河南", "新疆", "北京", "天津", "山东", "山西"]
    
    print(f"\n查找陈海勇负责的 12 个省份的专区:")
    for i, line in enumerate(lines):
        for province in chen_provinces:
            if province in line:
                print(f"行{i+1}: {line[:200]}")
                break
    
except Exception as e:
    print(f"错误：{e}")
