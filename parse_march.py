# -*- coding: utf-8 -*-
"""
分析 3 月份订单消息
"""

from datetime import datetime
import json

# 读取文件
with open('output/frame_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("=" * 80)
print("3 月份订单消息分析")
print("=" * 80)

march_items = []

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    
    # 查找 3 月份日期
    if '03-' in line:
        # 获取前一行（可能是标题）
        prev_line = lines[i-1].strip() if i > 0 else ''
        
        item = {
            'date': line,
            'title': prev_line,
            'full': f"{prev_line}\n{line}"
        }
        march_items.append(item)
        
        print(f"\n[项目 {len(march_items)}]")
        print(f"  标题：{prev_line[:100]}")
        print(f"  日期：{line}")

print("\n" + "=" * 80)
print(f"共找到 {len(march_items)} 条 3 月份记录")
print("=" * 80)

# 保存
with open('output/march_2026_items.json', 'w', encoding='utf-8') as f:
    json.dump(march_items, f, ensure_ascii=False, indent=2)

print(f"\n已保存：output/march_2026_items.json")

# 打印所有
print("\n[完整列表]")
for i, item in enumerate(march_items):
    print(f"{i+1}. {item['title'][:80]} - {item['date']}")
