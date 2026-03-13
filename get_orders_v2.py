# -*- coding: utf-8 -*-
"""
获取电商采购订单数据脚本 v2
- 改进表格选择器
- 支持多种表格结构
- 添加详细调试信息
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from datetime import datetime
import sys
import json

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 系统配置
LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/frame/fui/pages/themes/idea/idea?pageId=szcg-idea"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

# 筛选条件
TARGET_YEAR = 2026
TARGET_MONTH = 3  # 3月份

def get_orders():
    """获取订单数据"""
    print("=" * 80)
    print("[TEST] 电商采购订单数据获取 v2")
    print("=" * 80)
    print(f"登录地址：{LOGIN_URL}")
    print(f"订单页面：{ORDER_URL}")
    print(f"登录账号：{USERNAME}")
    print(f"筛选条件：{TARGET_YEAR}年{TARGET_MONTH}月")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    orders_data = []
    
    with sync_playwright() as p:
        # 启动浏览器
        print("\n[INFO] 启动浏览器...")
        browser = p.chromium.launch(headless=False, slow_mo=300)
        
        # 创建上下文
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 创建页面
        page = context.new_page()
        
        try:
            # ========== 1. 登录 ==========
            print("\n" + "=" * 80)
            print("[STEP 1] 登录系统")
            print("=" * 80)
            
            print(f"[INFO] 访问登录页面：{LOGIN_URL}")
            page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
            print("[OK] 登录页面加载完成")
            
            # 查找登录表单
            username_input = page.query_selector('input[type="text"]')
            password_input = page.query_selector('input[type="password"]')
            login_button = page.query_selector('.login-btn')
            
            if username_input and password_input and login_button:
                print("\n[INFO] 开始登录...")
                username_input.fill(USERNAME)
                password_input.fill(PASSWORD)
                time.sleep(1)
                login_button.click()
                print("[OK] 登录完成")
                time.sleep(2)
            else:
                print("[ERROR] 未找到登录表单元素")
                return
            
            # ========== 2. 访问订单页面 ==========
            print("\n" + "=" * 80)
            print("[STEP 2] 访问订单管理页面")
            print("=" * 80)
            
            print(f"[INFO] 访问页面：{ORDER_URL}")
            page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
            print("[OK] 订单页面加载完成")
            time.sleep(3)
            
            # ========== 3. 点击左侧菜单 ==========
            print("\n" + "=" * 80)
            print("[STEP 3] 点击左侧菜单：电商采购 -> 订单管理")
            print("=" * 80)
            
            try:
                ecommerce_menu = page.query_selector('text=电商采购')
                if ecommerce_menu:
                    ecommerce_menu.click()
                    time.sleep(1)
                
                order_menu = page.query_selector('text=订单管理')
                if order_menu:
                    order_menu.click()
                    time.sleep(2)
                
                page.wait_for_load_state("networkidle", timeout=10000)
                print("[OK] 菜单点击完成")
                
            except Exception as e:
                print(f"[WARN] 点击菜单失败：{e}")
            
            time.sleep(2)
            
            # ========== 4. 获取订单数据 ==========
            print("\n" + "=" * 80)
            print("[STEP 4] 获取订单数据")
            print("=" * 80)
            
            # 截图
            screenshot_path = "output/order_page_v2.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存截图：{screenshot_path}")
            
            # 保存页面 HTML 用于调试
            html_path = "output/order_page.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"[OK] 已保存 HTML: {html_path}")
            
            # 查找订单列表 - 多种选择器
            print("\n[INFO] 查找订单列表...")
            
            selectors_to_try = [
                'tr',  # 所有表格行
                'table tr',
                '.ant-table-row',
                '.el-table__row',
                '[class*="table"] tr',
                '[class*="order"] tr',
                '[class*="list"] tr',
                'tbody tr',
            ]
            
            order_rows = []
            for selector in selectors_to_try:
                rows = page.query_selector_all(selector)
                if len(rows) > 0:
                    print(f"[INFO] 选择器 '{selector}' 找到 {len(rows)} 行")
                    if len(rows) > len(order_rows):
                        order_rows = rows
            
            print(f"[INFO] 最佳选择器找到 {len(order_rows)} 行")
            
            # 遍历订单行
            for i, row in enumerate(order_rows[:100]):  # 最多处理100条
                try:
                    text_content = row.inner_text()
                    
                    # 检查是否包含3月份日期
                    date_patterns = [
                        f"{TARGET_YEAR}年{TARGET_MONTH:02d}月",
                        f"{TARGET_YEAR}-{TARGET_MONTH:02d}-",
                        f"{TARGET_YEAR}/{TARGET_MONTH:02d}/",
                        f"2026-03-",
                        f"2026/03/",
                    ]
                    
                    is_march_order = any(pattern in text_content for pattern in date_patterns)
                    
                    if is_march_order:
                        order_info = {
                            'index': i + 1,
                            'raw_text': text_content[:1000],
                            'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # 尝试提取订单编号
                        order_no_elem = row.query_selector('[class*="order-no"], [class*="orderNumber"], [class*="code"]')
                        if order_no_elem:
                            order_info['order_no'] = order_no_elem.inner_text().strip()
                        
                        # 尝试提取供应商
                        supplier_elem = row.query_selector('[class*="supplier"], [class*="vendor"], [class*="company"]')
                        if supplier_elem:
                            order_info['supplier'] = supplier_elem.inner_text().strip()
                        
                        # 尝试提取创建日期
                        date_elem = row.query_selector('[class*="date"], [class*="time"], [class*="create"]')
                        if date_elem:
                            order_info['create_date'] = date_elem.inner_text().strip()
                        
                        # 尝试提取订单状态
                        status_elem = row.query_selector('[class*="status"], .ant-tag, .el-tag, [class*="badge"]')
                        if status_elem:
                            order_info['status'] = status_elem.inner_text().strip()
                        
                        orders_data.append(order_info)
                        print(f"[OK] 订单 {len(orders_data)}: {order_info.get('order_no', 'N/A')}")
                        
                except Exception as e:
                    print(f"[WARN] 处理订单行 {i+1} 失败：{e}")
                    continue
            
            print(f"\n[OK] 共获取 {len(orders_data)} 条3月份订单")
            
            # ========== 5. 保存数据 ==========
            print("\n" + "=" * 80)
            print("[STEP 5] 保存数据")
            print("=" * 80)
            
            # 保存为 JSON
            json_path = "output/orders_202603_v2.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] 已保存 JSON: {json_path}")
            
            # 保存为 Excel
            try:
                import pandas as pd
                df = pd.DataFrame(orders_data)
                excel_path = "output/orders_202603_v2.xlsx"
                df.to_excel(excel_path, index=False)
                print(f"[OK] 已保存 Excel: {excel_path}")
            except ImportError:
                print("[INFO] 未安装 pandas，跳过 Excel 导出")
            
            # 打印摘要
            print("\n" + "=" * 80)
            print("[SUMMARY] 订单数据摘要")
            print("=" * 80)
            for order in orders_data[:20]:  # 显示前20条
                print(f"\n订单 {order.get('index', '?')}:")
                print(f"  订单编号：{order.get('order_no', 'N/A')}")
                print(f"  供应商：{order.get('supplier', 'N/A')}")
                print(f"  创建日期：{order.get('create_date', 'N/A')}")
                print(f"  状态：{order.get('status', 'N/A')}")
            
            print("\n" + "=" * 80)
            print(f"[DONE] 任务完成 - 共获取 {len(orders_data)} 条订单")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] 任务失败：{e}")
            import traceback
            traceback.print_exc()
            
            screenshot_path = "output/order_error_v2.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存错误页面截图：{screenshot_path}")
            
        finally:
            print("\n[INFO] 关闭浏览器...")
            browser.close()
            print("[OK] 浏览器已关闭")
    
    return orders_data


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    
    get_orders()
