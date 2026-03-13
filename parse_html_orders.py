# -*- coding: utf-8 -*-
"""
从 HTML 中提取 3 月份订单数据
"""

import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

# 读取 HTML
with open('output/order_page_full.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=" * 80)
print("从 HTML 中提取 3 月份订单")
print("=" * 80)

soup = BeautifulSoup(html, 'html.parser')

orders = []

# 查找所有订单项
order_items = soup.find_all('div', class_='order-item')
print(f"找到 {len(order_items)} 个订单项")

for i, item in enumerate(order_items):
    try:
        # 提取订单编号
        order_no_elem = item.find('div', class_='order-txt', string=re.compile('订单编号'))
        order_no = order_no_elem.get_text(strip=True) if order_no_elem else ''
        
        # 提取供应商
        supplier_elems = item.find_all('div', class_='order-txt')
        supplier = ''
        for elem in supplier_elems:
            if '供应商' in elem.get_text():
                supplier = elem.get_text(strip=True)
                break
        
        # 提取创建日期
        date_elem = None
        for elem in supplier_elems:
            if '创建日期' in elem.get_text():
                date_elem = elem
                break
        create_date = date_elem.get_text(strip=True) if date_elem else ''
        
        # 提取订单状态
        status_elem = item.find('span', class_='order-state')
        status = status_elem.get_text(strip=True) if status_elem else ''
        
        # 检查是否是 3 月份
        is_march = False
        # 多种日期格式匹配
        if any(pattern in create_date for pattern in ['2026 年 03 月', '2026-03-', '03 月', '2026/03/', '03/2026']):
            is_march = True
        # 正则匹配
        if not is_march and re.search(r'2026.?03.?[\d:]+', create_date):
            is_march = True
        
        # 打印所有订单用于调试
        print(f"\n[订单 {i+1}] {create_date} - {'3 月' if is_march else '非 3 月'}")
        
        if is_march:
            # 提取商品信息
            product_name = ''
            product_elem = item.find('p', title=re.compile('商品名称'))
            if product_elem:
                product_name = product_elem.get('title', '')
            
            order_info = {
                'index': i + 1,
                'order_no': order_no.replace('订单编号：', '').strip(),
                'supplier': supplier.replace('供应商：', '').strip(),
                'create_date': create_date.replace('创建日期：', '').strip(),
                'status': status,
                'product': product_name.replace('商品名称：', '').strip()[:100],
                'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            orders.append(order_info)
            print(f"\n[订单 {len(orders)}]")
            print(f"  编号：{order_info['order_no']}")
            print(f"  供应商：{order_info['supplier']}")
            print(f"  日期：{order_info['create_date']}")
            print(f"  状态：{order_info['status']}")
            print(f"  商品：{order_info['product'][:50]}...")
            
    except Exception as e:
        print(f"[WARN] 处理订单 {i+1} 失败：{e}")
        continue

print("\n" + "=" * 80)
print(f"共找到 {len(orders)} 条 3 月份订单")
print("=" * 80)

# 保存
json_path = 'output/march_orders_from_html.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(orders, f, ensure_ascii=False, indent=2)
print(f"[OK] 已保存：{json_path}")

# Excel
try:
    import pandas as pd
    df = pd.DataFrame(orders)
    excel_path = 'output/march_orders_from_html.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"[OK] Excel: {excel_path}")
except:
    pass

# 打印所有
print("\n[完整列表]")
for i, order in enumerate(orders):
    print(f"\n{i+1}. {order['order_no']} | {order['supplier']} | {order['create_date']} | {order['status']}")
