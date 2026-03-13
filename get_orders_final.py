# -*- coding: utf-8 -*-
"""
获取 3 月份订单 - 最终版本
通过拦截和重放页面请求获取数据
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/zhongzi/purchasecontractordernew/order/order"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def get_orders_final():
    print("=" * 80)
    print("[获取] 3 月份订单数据 - 最终版本")
    print("=" * 80)
    
    march_orders = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        # 拦截 API 响应
        def handle_response(response):
            nonlocal march_orders
            if 'getOrder' in response.url and response.request.method == 'POST':
                try:
                    data = response.json()
                    if data and 'data' in data:
                        orders = data.get('data', {}).get('data', [])
                        if orders:
                            print(f"\n[API 响应] 获取到 {len(orders)} 条订单")
                            for order in orders:
                                create_date = order.get('createdate', '')
                                if '2026-03' in create_date or '2026 年 03 月' in create_date:
                                    march_orders.append(order)
                                    print(f"  - {order.get('orderNum', 'N/A')} | {create_date}")
                except:
                    pass
        
        page.on('response', handle_response)
        
        # 登录
        print("\n[1] 登录...")
        page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
        page.query_selector('input[type="text"]').fill(USERNAME)
        page.query_selector('input[type="password"]').fill(PASSWORD)
        time.sleep(1)
        page.query_selector('.login-btn').click()
        time.sleep(3)
        print("[OK] 登录完成")
        
        # 访问订单页面
        print("\n[2] 访问订单页面...")
        page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
        time.sleep(5)
        print(f"[OK] 页面加载完成，捕获到 {len(march_orders)} 条 3 月份订单")
        
        # 尝试设置日期筛选
        print("\n[3] 设置 3 月份日期筛选...")
        
        try:
            # 点击高级搜索
            search_btn = page.query_selector('text=高级搜索')
            if search_btn:
                search_btn.click()
                time.sleep(2)
                
                # 输入开始日期
                start_input = page.query_selector('#orderTime$text')
                if start_input:
                    start_input.fill('2026-03-01')
                    time.sleep(1)
                
                # 输入结束日期（可能需要选择结束日期）
                # 这里简化处理，直接搜索
                
                # 点击搜索按钮
                search_button = page.query_selector('text=搜索')
                if search_button:
                    search_button.click()
                    time.sleep(5)
                    print("[OK] 已设置日期筛选")
                    
        except Exception as e:
            print(f"[WARN] 设置筛选失败：{e}")
        
        print(f"\n[当前] 共捕获到 {len(march_orders)} 条 3 月份订单")
        
        # 从页面提取订单数据
        print("\n[4] 从页面提取订单数据...")
        
        page_orders = page.evaluate('''() => {
            const orders = [];
            const orderItems = document.querySelectorAll('.order-item');
            
            orderItems.forEach((item, index) => {
                const orderNoElem = item.querySelector('.order-txt');
                const supplierElems = item.querySelectorAll('.order-txt');
                const dateElem = item.querySelectorAll('.order-txt')[1];
                const statusElem = item.querySelector('.order-state');
                
                let orderNo = orderNoElem ? orderNoElem.textContent.replace('订单编号：', '').trim() : '';
                let supplier = '';
                let createDate = '';
                
                supplierElems.forEach(elem => {
                    const text = elem.textContent;
                    if (text.includes('供应商：')) supplier = text.replace('供应商：', '').trim();
                    if (text.includes('创建日期：')) createDate = text.replace('创建日期：', '').trim();
                });
                
                orders.push({
                    index: index + 1,
                    orderNum: orderNo,
                    supplier: supplier,
                    createDate: createDate,
                    status: statusElem ? statusElem.textContent.trim() : ''
                });
            });
            
            return orders;
        }''')
        
        print(f"    页面提取到 {len(page_orders)} 条订单")
        
        # 筛选 3 月份
        for order in page_orders:
            if '2026 年 03 月' in order['createDate'] or '2026-03-' in order['createDate']:
                order['captured_at'] = datetime.now().isoformat()
                march_orders.append(order)
                print(f"  + {order['orderNum']} | {order['createDate']}")
        
        # 去重
        seen = set()
        unique_orders = []
        for order in march_orders:
            key = order.get('orderNum', '')
            if key not in seen:
                seen.add(key)
                unique_orders.append(order)
        
        march_orders = unique_orders
        
        # 保存
        print(f"\n[5] 保存数据...")
        print(f"    共 {len(march_orders)} 条不重复的 3 月份订单")
        
        with open('output/march_orders_final.json', 'w', encoding='utf-8') as f:
            json.dump(march_orders, f, ensure_ascii=False, indent=2)
        print(f"[OK] JSON: output/march_orders_final.json")
        
        try:
            import pandas as pd
            df = pd.DataFrame(march_orders)
            df.to_excel('output/march_orders_final.xlsx', index=False)
            print(f"[OK] Excel: output/march_orders_final.xlsx")
        except:
            pass
        
        # 打印摘要
        print("\n" + "=" * 80)
        print("[3 月份订单摘要]")
        print("=" * 80)
        
        for i, order in enumerate(march_orders[:20]):
            print(f"\n{i+1}. {order.get('orderNum', 'N/A')}")
            print(f"   供应商：{order.get('supplier', 'N/A')}")
            print(f"   日期：{order.get('createDate', 'N/A')}")
            print(f"   状态：{order.get('status', 'N/A')}")
        
        print("\n" + "=" * 80)
        print(f"[完成] 共获取 {len(march_orders)} 条 3 月份订单")
        print("=" * 80)
        
        browser.close()
    
    return march_orders


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    get_orders_final()
