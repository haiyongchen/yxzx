# -*- coding: utf-8 -*-
"""
测试 API - 通过页面 JavaScript 调用
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/zhongzi/purchasecontractordernew/order/order"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def test_api_v3():
    print("=" * 80)
    print("[测试] 通过页面 JavaScript 调用 API")
    print("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
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
        print("[OK] 页面加载完成")
        
        # 从 HTML 中提取 API 调用信息
        print("\n[3] 分析页面中的 API 调用...")
        
        # 查找所有 fetch/XHR 请求
        api_calls = []
        
        def handle_request(request):
            if 'rest' in request.url or 'action' in request.url:
                api_calls.append({
                    'url': request.url,
                    'method': request.method,
                    'resourceType': request.resource_type
                })
        
        page.on('request', handle_request)
        
        # 触发页面刷新以捕获请求
        print("    刷新页面捕获请求...")
        page.reload(wait_until="networkidle")
        time.sleep(3)
        
        print(f"    捕获到 {len(api_calls)} 个 API 请求")
        for call in api_calls[:10]:
            print(f"      {call['method']} {call['url'][:150]}")
        
        # 保存
        with open('output/api_calls.json', 'w', encoding='utf-8') as f:
            json.dump(api_calls, f, ensure_ascii=False, indent=2)
        
        # 尝试使用页面内置函数调用
        print("\n[4] 使用页面内置函数调用 API...")
        
        try:
            # 尝试调用 getTabNum
            tabnum_result = page.evaluate('''() => {
                return new Promise((resolve) => {
                    if (typeof epoint !== 'undefined' && epoint.dealRestfulUrl) {
                        const url = epoint.dealRestfulUrl('zhongzicgrmallpurchasecontractorderlistaction/getTabNum');
                        
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', url, true);
                        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                        
                        xhr.onload = function() {
                            try {
                                resolve({
                                    success: true,
                                    url: url,
                                    status: xhr.status,
                                    data: JSON.parse(xhr.responseText)
                                });
                            } catch (e) {
                                resolve({
                                    success: true,
                                    url: url,
                                    status: xhr.status,
                                    text: xhr.responseText.substring(0, 300)
                                });
                            }
                        };
                        
                        xhr.onerror = function() {
                            resolve({ success: false, error: 'Network error' });
                        };
                        
                        xhr.send();
                    } else {
                        resolve({ error: 'epoint.dealRestfulUrl not found' });
                    }
                });
            }''')
            
            print(f"    getTabNum 结果：{json.dumps(tabnum_result, ensure_ascii=False, default=str)[:300]}")
            
        except Exception as e:
            print(f"    [ERROR] {e}")
        
        # 尝试获取订单列表（带 3 月份筛选）
        print("\n[5] 获取 3 月份订单...")
        
        try:
            order_result = page.evaluate('''() => {
                return new Promise((resolve) => {
                    if (typeof epoint !== 'undefined' && epoint.dealRestfulUrl) {
                        const url = epoint.dealRestfulUrl('zhongzicgrmallpurchasecontractorderlistaction/getOrder');
                        
                        const xhr = new XMLHttpRequest();
                        xhr.open('POST', url, true);
                        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                        
                        xhr.onload = function() {
                            try {
                                resolve({
                                    success: true,
                                    url: url,
                                    status: xhr.status,
                                    data: JSON.parse(xhr.responseText)
                                });
                            } catch (e) {
                                resolve({
                                    success: true,
                                    url: url,
                                    status: xhr.status,
                                    text: xhr.responseText.substring(0, 500)
                                });
                            }
                        };
                        
                        xhr.onerror = function() {
                            resolve({ success: false, error: 'Network error' });
                        };
                        
                        // 带 3 月份筛选参数
                        const params = 'start=0&limit=50&orderTime1=2026-03-01&orderTime2=2026-03-31';
                        xhr.send(params);
                    } else {
                        resolve({ error: 'epoint.dealRestfulUrl not found' });
                    }
                });
            }''')
            
            print(f"    订单查询结果：{json.dumps(order_result, ensure_ascii=False, default=str)[:500]}")
            
            # 保存完整结果
            with open('output/api_order_march.json', 'w', encoding='utf-8') as f:
                json.dump(order_result, f, ensure_ascii=False, indent=2, default=str)
            print(f"[OK] 结果已保存：output/api_order_march.json")
            
        except Exception as e:
            print(f"    [ERROR] {e}")
        
        browser.close()
        print("\n[OK] 测试完成")


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    test_api_v3()
