# -*- coding: utf-8 -*-
"""
测试直接访问订单 API
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/zhongzi/purchasecontractordernew/order/order"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def test_api():
    print("=" * 80)
    print("[测试] 直接访问订单 API")
    print("=" * 80)
    
    with sync_playwright() as p:
        # 启动浏览器
        print("\n[1] 启动浏览器并登录...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        # 登录
        page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
        page.query_selector('input[type="text"]').fill(USERNAME)
        page.query_selector('input[type="password"]').fill(PASSWORD)
        time.sleep(1)
        page.query_selector('.login-btn').click()
        time.sleep(3)
        print("[OK] 登录完成")
        
        # 访问订单页面
        print("\n[2] 访问订单页面获取 API 信息...")
        page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
        time.sleep(5)
        
        # 获取 cookies
        cookies = context.cookies()
        print(f"[OK] 获取到 {len(cookies)} 个 cookies")
        
        # 保存 cookies
        with open('output/cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"[OK] Cookies 已保存：output/cookies.json")
        
        # 获取页面中的 API 配置
        api_config = page.evaluate('''() => {
            return {
                pageConfig: window.pageConfig || {},
                baseUrl: window.location.origin
            };
        }''')
        
        print("\n[3] API 配置:")
        print(f"    Base URL: {api_config.get('baseUrl', 'N/A')}")
        if 'pageConfig' in api_config:
            for key, value in api_config['pageConfig'].items():
                print(f"    {key}: {value}")
        
        # 尝试直接调用 API
        print("\n[4] 尝试调用 API...")
        
        # 使用 page.evaluate 执行 JavaScript 调用 API
        try:
            api_result = page.evaluate('''() => {
                return new Promise((resolve, reject) => {
                    // 尝试获取订单列表
                    const xhr = new XMLHttpRequest();
                    xhr.open('POST', '/qytpframe_cs/rest/zhongzicgrmallpurchasecontractorderlistaction/getOrder', true);
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                    
                    xhr.onload = function() {
                        if (xhr.status === 200) {
                            try {
                                resolve(JSON.parse(xhr.responseText));
                            } catch (e) {
                                resolve({ text: xhr.responseText.substring(0, 500) });
                            }
                        } else {
                            reject({ status: xhr.status, text: xhr.responseText });
                        }
                    };
                    
                    xhr.onerror = function() {
                        reject({ error: 'Network error' });
                    };
                    
                    // 发送请求 - 尝试获取 3 月份订单
                    const params = 'start=0&limit=10&orderTime1=2026-03-01&orderTime2=2026-03-31';
                    xhr.send(params);
                });
            }''')
            
            print("[OK] API 调用成功!")
            print(f"    响应类型：{type(api_result)}")
            
            # 保存结果
            with open('output/api_result.json', 'w', encoding='utf-8') as f:
                json.dump(api_result, f, ensure_ascii=False, indent=2, default=str)
            print(f"[OK] 结果已保存：output/api_result.json")
            
            # 打印部分结果
            if isinstance(api_result, dict):
                print(f"\n    键：{list(api_result.keys())[:10]}")
            
        except Exception as e:
            print(f"[WARN] API 调用失败：{e}")
            
            # 尝试不带参数的简单调用
            print("\n[5] 尝试简单 API 调用...")
            try:
                simple_result = page.evaluate('''() => {
                    return new Promise((resolve) => {
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', '/qytpframe_cs/rest/zhongzicgrmallpurchasecontractorderlistaction/getTabNum', true);
                        xhr.onload = function() {
                            try {
                                resolve({ status: xhr.status, data: JSON.parse(xhr.responseText) });
                            } catch (e) {
                                resolve({ status: xhr.status, text: xhr.responseText.substring(0, 300) });
                            }
                        };
                        xhr.onerror = function() {
                            resolve({ error: 'Network error' });
                        };
                        xhr.send();
                    });
                }''')
                
                print(f"[OK] 简单调用结果：{simple_result}")
                
            except Exception as e2:
                print(f"[WARN] 简单调用也失败：{e2}")
        
        browser.close()
        print("\n[OK] 测试完成")


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    test_api()
