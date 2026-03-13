# -*- coding: utf-8 -*-
"""
获取电商采购订单数据脚本
- 登录系统
- 访问订单管理页面
- 获取3月份订单数据
- 导出为 Excel
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
    print("[TEST] 电商采购订单数据获取")
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
            login_selectors = ['input[type="text"]']
            password_selectors = ['input[type="password"]']
            button_selectors = ['.login-btn']
            
            username_input = None
            for selector in login_selectors:
                username_input = page.query_selector(selector)
                if username_input:
                    print(f"[OK] 找到用户名输入框：{selector}")
                    break
            
            password_input = None
            for selector in password_selectors:
                password_input = page.query_selector(selector)
                if password_input:
                    print(f"[OK] 找到密码输入框：{selector}")
                    break
            
            login_button = None
            for selector in button_selectors:
                login_button = page.query_selector(selector)
                if login_button:
                    print(f"[OK] 找到登录按钮：{selector}")
                    break
            
            if username_input and password_input and login_button:
                print("\n[INFO] 开始登录...")
                username_input.fill(USERNAME)
                print(f"   已输入用户名：{USERNAME}")
                
                password_input.fill(PASSWORD)
                print(f"   已输入密码：{'*' * len(PASSWORD)}")
                
                time.sleep(1)
                login_button.click()
                print("   已点击登录按钮")
                
                print("\n[INFO] 等待登录完成...")
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                    print("[OK] 登录完成")
                except PlaywrightTimeout:
                    print("[WARN] 登录等待超时")
                
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
            
            # 截图
            screenshot_path = "output/order_page_before.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存截图：{screenshot_path}")
            
            time.sleep(3)
            
            # ========== 3. 点击左侧菜单 ==========
            print("\n" + "=" * 80)
            print("[STEP 3] 点击左侧菜单：电商采购 -> 订单管理")
            print("=" * 80)
            
            # 尝试点击左侧菜单
            try:
                # 先找"电商采购"菜单
                print("[INFO] 查找'电商采购'菜单...")
                ecommerce_menu = page.query_selector('text=电商采购')
                if ecommerce_menu:
                    print("[OK] 找到'电商采购'菜单")
                    ecommerce_menu.click()
                    print("[OK] 已点击'电商采购'")
                    time.sleep(1)
                else:
                    print("[WARN] 未找到'电商采购'菜单，可能已展开")
                
                # 再找"订单管理"菜单
                print("[INFO] 查找'订单管理'菜单...")
                order_menu = page.query_selector('text=订单管理')
                if order_menu:
                    print("[OK] 找到'订单管理'菜单")
                    order_menu.click()
                    print("[OK] 已点击'订单管理'")
                    time.sleep(2)
                else:
                    print("[WARN] 未找到'订单管理'菜单，可能已在订单页面")
                
                # 等待页面加载
                page.wait_for_load_state("networkidle", timeout=10000)
                print("[OK] 菜单点击完成")
                
            except Exception as e:
                print(f"[WARN] 点击菜单失败：{e}")
                print("[INFO] 可能已在订单页面，继续...")
            
            time.sleep(2)
            
            # ========== 4. 获取订单数据 ==========
            print("\n" + "=" * 80)
            print("[STEP 4] 获取订单数据")
            print("=" * 80)
            
            # 截图
            screenshot_path = "output/order_page_after.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存截图：{screenshot_path}")
            
            # 尝试获取订单列表
            print("\n[INFO] 查找订单列表...")
            
            # 查找订单行（常见的表格行选择器）
            order_rows = page.query_selector_all('tr.ant-table-row, tr.el-table__row, .order-row, [class*="order"] tr')
            print(f"[INFO] 找到 {len(order_rows)} 个订单行")
            
            # 遍历订单行
            for i, row in enumerate(order_rows[:50]):  # 最多处理50条
                try:
                    # 获取订单文本内容
                    text_content = row.inner_text()
                    
                    # 检查是否包含3月份日期
                    date_str = f"{TARGET_YEAR}年{TARGET_MONTH:02d}月"
                    if date_str in text_content or f"2026-03-" in text_content or f"2026/03/" in text_content:
                        # 提取订单信息
                        order_info = {
                            'index': i + 1,
                            'raw_text': text_content[:500],  # 限制长度
                            'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # 尝试提取订单编号
                        order_no_elem = row.query_selector('[class*="order-no"], [class*="orderNumber"]')
                        if order_no_elem:
                            order_info['order_no'] = order_no_elem.inner_text()
                        
                        # 尝试提取供应商
                        supplier_elem = row.query_selector('[class*="supplier"], [class*="vendor"]')
                        if supplier_elem:
                            order_info['supplier'] = supplier_elem.inner_text()
                        
                        # 尝试提取创建日期
                        date_elem = row.query_selector('[class*="date"], [class*="time"]')
                        if date_elem:
                            order_info['create_date'] = date_elem.inner_text()
                        
                        # 尝试提取订单状态
                        status_elem = row.query_selector('[class*="status"], .ant-tag, .el-tag')
                        if status_elem:
                            order_info['status'] = status_elem.inner_text()
                        
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
            import json
            json_path = "output/orders_202603.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] 已保存 JSON: {json_path}")
            
            # 保存为 Excel (如果有 pandas)
            try:
                import pandas as pd
                df = pd.DataFrame(orders_data)
                excel_path = "output/orders_202603.xlsx"
                df.to_excel(excel_path, index=False)
                print(f"[OK] 已保存 Excel: {excel_path}")
            except ImportError:
                print("[INFO] 未安装 pandas，跳过 Excel 导出")
                print("[INFO] 运行以下命令安装：pip install pandas openpyxl")
            
            # 打印摘要
            print("\n" + "=" * 80)
            print("[SUMMARY] 订单数据摘要")
            print("=" * 80)
            for order in orders_data[:10]:  # 显示前10条
                print(f"\n订单 {order.get('index', '?')}:")
                print(f"  订单编号：{order.get('order_no', 'N/A')}")
                print(f"  供应商：{order.get('supplier', 'N/A')}")
                print(f"  创建日期：{order.get('create_date', 'N/A')}")
                print(f"  状态：{order.get('status', 'N/A')}")
            
            print("\n" + "=" * 80)
            print("[DONE] 任务完成")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] 任务失败：{e}")
            import traceback
            traceback.print_exc()
            
            # 截图保存错误页面
            screenshot_path = "output/order_error.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存错误页面截图：{screenshot_path}")
            
        finally:
            # 关闭浏览器
            print("\n[INFO] 关闭浏览器...")
            browser.close()
            print("[OK] 浏览器已关闭")
    
    return orders_data


if __name__ == '__main__':
    # 确保输出目录存在
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    
    get_orders()
