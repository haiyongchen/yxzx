# -*- coding: utf-8 -*-
"""
爬取电商采购订单数据
直接访问订单管理页面
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import json
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 系统配置
LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/zhongzi/purchasecontractordernew/order/order"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def crawl_orders():
    print("=" * 80)
    print("[爬取] 电商采购订单数据")
    print("=" * 80)
    print(f"登录地址：{LOGIN_URL}")
    print(f"订单地址：{ORDER_URL}")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    orders_data = []
    
    with sync_playwright() as p:
        # 启动浏览器
        print("\n[1] 启动浏览器...")
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            # 登录
            print("\n[2] 登录系统...")
            page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
            page.query_selector('input[type="text"]').fill(USERNAME)
            page.query_selector('input[type="password"]').fill(PASSWORD)
            time.sleep(1)
            page.query_selector('.login-btn').click()
            time.sleep(2)
            print("[OK] 登录完成")
            
            # 访问订单页面
            print("\n[3] 访问订单管理页面...")
            page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
            time.sleep(5)  # 等待动态加载
            print("[OK] 页面加载完成")
            
            # 截图
            screenshot_path = f"output/orders_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 截图：{screenshot_path}")
            
            # 保存 HTML
            html_path = "output/order_page_full.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"[OK] HTML: {html_path}")
            
            # 检查 iframe
            print("\n[4] 分析页面结构...")
            frames = page.frames
            print(f"    找到 {len(frames)} 个 frame")
            
            # 在所有 frame 中查找订单数据
            all_text_content = []
            
            for i, frame in enumerate(frames):
                try:
                    frame_text = frame.inner_text('body', timeout=5000)
                    if frame_text and len(frame_text) > 50:
                        all_text_content.append({
                            'frame_index': i,
                            'url': frame.url[:150],
                            'text': frame_text
                        })
                        print(f"    Frame {i}: {len(frame_text)} 字符")
                except Exception as e:
                    continue
            
            # 提取 3 月份订单
            print("\n[5] 提取 3 月份订单...")
            
            march_orders = []
            
            for frame_info in all_text_content:
                text = frame_info['text']
                lines = text.split('\n')
                
                for j, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查是否包含 3 月份
                    if '2026-03-' in line or '2026/03/' in line or '03-0' in line or '03-1' in line or '03-2' in line or '03-3' in line:
                        # 检查是否是订单相关
                        if any(keyword in line for keyword in ['订单', '采购', '合同', '供应商', '金额', '编号', '批次']):
                            # 获取上下文
                            context_start = max(0, j-3)
                            context_end = min(len(lines), j+4)
                            context = '\n'.join([lines[k].strip() for k in range(context_start, context_end)])
                            
                            order = {
                                'frame': frame_info['frame_index'],
                                'line': j,
                                'content': line,
                                'context': context,
                                'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            march_orders.append(order)
                            print(f"    [OK] 找到订单：{line[:80]}")
            
            orders_data = march_orders
            
            print(f"\n[OK] 共找到 {len(orders_data)} 条 3 月份订单")
            
            # 保存数据
            print("\n[6] 保存数据...")
            
            # JSON
            json_path = f"output/march_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] JSON: {json_path}")
            
            # Excel
            try:
                import pandas as pd
                df = pd.DataFrame(orders_data)
                excel_path = f"output/march_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(excel_path, index=False)
                print(f"[OK] Excel: {excel_path}")
            except ImportError:
                print("[INFO] 未安装 pandas，跳过 Excel")
            
            # 打印摘要
            print("\n" + "=" * 80)
            print("[订单摘要]")
            print("=" * 80)
            
            for i, order in enumerate(orders_data[:30]):
                print(f"\n{i+1}. {order['content'][:120]}")
            
            print("\n" + "=" * 80)
            print(f"[完成] 共爬取 {len(orders_data)} 条订单")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
            
            # 错误截图
            error_path = "output/crawl_error.png"
            page.screenshot(path=error_path, full_page=True)
            print(f"[OK] 错误截图：{error_path}")
            
        finally:
            browser.close()
            print("\n[OK] 浏览器已关闭")
    
    return orders_data


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    crawl_orders()
