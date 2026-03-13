# -*- coding: utf-8 -*-
"""
获取电商采购订单数据脚本 v5
- 从"我的消息"中提取 3 月份订单相关消息
- 已找到 3 月份数据！
"""

from datetime import datetime
import json
import re

# 读取之前保存的文本
with open('output/frame_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("[分析] 从'我的消息'中提取订单数据")
print("=" * 80)

# 按行分割
lines = content.split('\n')

# 查找 3 月份的订单
march_orders = []

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    
    # 检查是否包含 3 月份日期
    if '03-' in line or '03 月' in line:
        # 检查是否是订单相关
        if '订单' in line or '采购' in line or '退货' in line or '审核' in line:
            # 获取上下文
            context_start = max(0, i-1)
            context_end = min(len(lines), i+2)
            context = '\n'.join([lines[j].strip() for j in range(context_start, context_end)])
            
            order_info = {
                'line': i,
                'content': line,
                'context': context,
                'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            march_orders.append(order_info)
            print(f"\n[订单 {len(march_orders)}]")
            print(f"  内容：{line}")
            if context_start != i:
                print(f"  上下文：{lines[context_start].strip() if context_start != i else ''}")

print("\n" + "=" * 80)
print(f"[结果] 共找到 {len(march_orders)} 条 3 月份订单相关消息")
print("=" * 80)

# 保存
output_path = 'output/march_orders_from_messages.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(march_orders, f, ensure_ascii=False, indent=2)
print(f"[OK] 已保存：{output_path}")

# 打印详情
print("\n[详情]")
for i, order in enumerate(march_orders):
    print(f"\n{i+1}. {order['content']}")
