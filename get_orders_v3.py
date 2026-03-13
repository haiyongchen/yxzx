# -*- coding: utf-8 -*-
"""
获取电商采购订单数据脚本 v3
- 处理 iframe 嵌套
- 等待动态内容加载
- 详细调试输出
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from datetime import datetime
import sys
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 系统配置
LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/frame/fui/pages/themes/idea/idea?pageId=szcg-idea"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

TARGET_YEAR = 2026
TARGET_MONTH = 3

def get_orders():
    """获取订单数据"""
    print("=" * 80)
    print("[TEST] 电商采购订单数据获取 v3 (iframe 支持)")
    print("=" * 80)
    
    orders_data = []
    
    with sync_playwright() as p:
        print("\n[INFO] 启动浏览器...")
        browser = p.chromium.launch(headless=False, slow_mo=300)
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = context.new_page()
        
        try:
            # ========== 1. 登录 ==========
            print("\n[STEP 1] 登录系统")
            page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
            username_input = page.query_selector('input[type="text"]')
            password_input = page.query_selector('input[type="password"]')
            login_button = page.query_selector('.login-btn')
            
            if username_input and password_input and login_button:
                username_input.fill(USERNAME)
                password_input.fill(PASSWORD)
                time.sleep(1)
                login_button.click()
                time.sleep(2)
                print("[OK] 登录完成")
            
            # ========== 2. 访问订单页面 ==========
            print("\n[STEP 2] 访问订单页面")
            page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
            time.sleep(5)  # 等待更长时间
            
            # 截图
            page.screenshot(path="output/order_page_v3.png", full_page=True)
            print("[OK] 已保存截图")
            
            # ========== 3. 检查 iframe ==========
            print("\n[STEP 3] 检查 iframe...")
            frames = page.frames
            print(f"[INFO] 找到 {len(frames)} 个 frame")
            
            for i, frame in enumerate(frames):
                print(f"  Frame {i}: {frame.url[:100]}...")
            
            # ========== 4. 在 main frame 和子 frame 中查找表格 ==========
            print("\n[STEP 4] 查找订单表格...")
            
            # 尝试在主页面和所有 iframe 中查找
            frames_to_search = [page] + list(frames[1:]) if len(frames) > 1 else [page]
            
            for frame_idx, frame in enumerate(frames_to_search):
                print(f"\n[INFO] 搜索 Frame {frame_idx}...")
                
                # 查找所有表格
                tables = frame.query_selector_all('table')
                print(f"  找到 {len(tables)} 个表格")
                
                # 查找所有行
                rows = frame.query_selector_all('tr')
                print(f"  找到 {len(rows)} 个行")
                
                # 查找包含"订单"文本的元素
                order_elements = frame.query_selector_all('text=订单')
                print(f"  找到 {len(order_elements)} 个包含'订单'的元素")
                
                # 遍历所有行
                for i, row in enumerate(rows[:200]):
                    try:
                        text = row.inner_text(timeout=5000)
                        
                        # 检查是否包含 3 月份
                        if f"2026-03-" in text or f"2026/03/" in text or "26 年 03 月" in text or "2026 年 03 月" in text:
                            order_info = {
                                'frame': frame_idx,
                                'row': i,
                                'text': text[:1000],
                                'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            # 尝试提取关键信息
                            cells = row.query_selector_all('td, th')
                            if len(cells) > 0:
                                order_info['cells_count'] = len(cells)
                                order_info['cell_texts'] = [cell.inner_text().strip() for cell in cells[:10]]
                            
                            orders_data.append(order_info)
                            print(f"  [OK] 找到 3 月订单：行{i}")
                            
                    except Exception as e:
                        continue
            
            print(f"\n[OK] 共获取 {len(orders_data)} 条 3 月份订单")
            
            # ========== 5. 保存数据 ==========
            print("\n[STEP 5] 保存数据")
            
            json_path = "output/orders_202603_v3.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] JSON: {json_path}")
            
            try:
                import pandas as pd
                df = pd.DataFrame(orders_data)
                excel_path = "output/orders_202603_v3.xlsx"
                df.to_excel(excel_path, index=False)
                print(f"[OK] Excel: {excel_path}")
            except:
                pass
            
            # 打印详情
            print("\n" + "=" * 80)
            print("[订单详情]")
            print("=" * 80)
            for order in orders_data[:30]:
                print(f"\nFrame {order.get('frame', '?')}, 行 {order.get('row', '?')}:")
                cells = order.get('cell_texts', [])
                for j, cell in enumerate(cells):
                    if cell:
                        print(f"  列{j}: {cell[:100]}")
            
            print("\n" + "=" * 80)
            print(f"[DONE] 完成 - 共 {len(orders_data)} 条订单")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            browser.close()
            print("\n[OK] 浏览器已关闭")
    
    return orders_data


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    get_orders()
