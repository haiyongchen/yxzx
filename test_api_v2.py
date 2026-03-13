# -*- coding: utf-8 -*-
"""
测试 API - 获取授权 token
"""

from playwright.sync_api import sync_playwright
import time
import json
import requests
from datetime import datetime

LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/zhongzi/purchasecontractordernew/order/order"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def test_api_v2():
    print("=" * 80)
    print("[测试] API 授权访问")
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
        
        # 获取所有 storage
        print("\n[3] 获取认证信息...")
        
        # LocalStorage
        local_storage = page.evaluate("() => Object.entries(localStorage).map(([k,v]) => ({key:k, value:v}))")
        print(f"    LocalStorage: {len(local_storage)} 项")
        
        # 查找可能包含 token 的项
        for item in local_storage[:20]:
            key = item.get('key', '')
            value = item.get('value', '')
            if any(k in key.lower() for k in ['token', 'auth', 'user', 'session']):
                print(f"      {key[:50]}: {value[:100]}...")
        
        # 获取 cookies
        cookies = context.cookies()
        print(f"\n    Cookies: {len(cookies)} 个")
        for cookie in cookies:
            if any(k in cookie['name'].lower() for k in ['token', 'auth', 'session', 'user']):
                print(f"      {cookie['name']}: {cookie['value'][:100]}...")
        
        # 保存认证信息
        auth_info = {
            'cookies': cookies,
            'local_storage': local_storage,
            'url': page.url,
            'captured_at': datetime.now().isoformat()
        }
        
        with open('output/auth_info.json', 'w', encoding='utf-8') as f:
            json.dump(auth_info, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n[OK] 认证信息已保存：output/auth_info.json")
        
        # 使用 requests 测试 API
        print("\n[4] 使用 requests 测试 API...")
        
        # 构建 session
        session = requests.Session()
        
        # 添加 cookies
        base_url = "https://dev-ec.cneptp.com:10081"
        for cookie in cookies:
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', 'dev-ec.cneptp.com'),
                path=cookie.get('path', '/')
            )
        
        # 测试 API
        api_url = f"{base_url}/qytpframe_cs/rest/zhongzicgrmallpurchasecontractorderlistaction/getTabNum"
        
        print(f"    API: {api_url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': ORDER_URL,
            }
            
            response = session.get(api_url, headers=headers, timeout=10, verify=False)
            print(f"    状态码：{response.status_code}")
            print(f"    响应长度：{len(response.text)}")
            
            try:
                result = response.json()
                print(f"    响应：{json.dumps(result, ensure_ascii=False)[:300]}")
                
                # 保存
                with open('output/api_tabnum_result.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"[OK] 结果已保存：output/api_tabnum_result.json")
                
            except:
                print(f"    响应文本：{response.text[:300]}")
                
        except requests.exceptions.SSLError:
            print("    [WARN] SSL 错误，尝试禁用验证...")
        except Exception as e:
            print(f"    [ERROR] {e}")
        
        # 测试带参数的订单查询
        print("\n[5] 测试订单查询 API...")
        
        order_api = f"{base_url}/qytpframe_cs/rest/zhongzicgrmallpurchasecontractorderlistaction/getOrder"
        
        try:
            params = {
                'start': '0',
                'limit': '10',
                'orderTime1': '2026-03-01',
                'orderTime2': '2026-03-31',
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': ORDER_URL,
                'X-Requested-With': 'XMLHttpRequest',
            }
            
            response = session.post(order_api, headers=headers, data=params, timeout=10, verify=False)
            print(f"    状态码：{response.status_code}")
            
            try:
                result = response.json()
                print(f"    响应：{json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
                
                with open('output/api_order_result.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2, default=str)
                print(f"[OK] 结果已保存：output/api_order_result.json")
                
            except Exception as e:
                print(f"    解析失败：{e}")
                print(f"    响应：{response.text[:500]}")
                
        except Exception as e:
            print(f"    [ERROR] {e}")
        
        browser.close()
        print("\n[OK] 测试完成")


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    import requests
    requests.packages.urllib3.disable_warnings()  # 禁用 SSL 警告
    test_api_v2()
