# -*- coding: utf-8 -*-
"""
获取电商采购订单数据脚本 v4
- 定位到正确的 iframe (Frame 5)
- 等待内容加载
- 获取订单数据
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import sys
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

LOGIN_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
ORDER_URL = "https://dev-ec.cneptp.com:10081/qytpframe_cs/frame/fui/pages/themes/idea/idea?pageId=szcg-idea"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def get_orders():
    print("=" * 80)
    print("[TEST] 电商采购订单数据获取 v4 (定位 iframe)")
    print("=" * 80)
    
    orders_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            # 登录
            print("\n[1] 登录...")
            page.goto(LOGIN_URL, timeout=30000, wait_until="networkidle")
            page.query_selector('input[type="text"]').fill(USERNAME)
            page.query_selector('input[type="password"]').fill(PASSWORD)
            time.sleep(1)
            page.query_selector('.login-btn').click()
            time.sleep(2)
            print("[OK] 登录完成")
            
            # 访问订单页面
            print("\n[2] 访问订单页面...")
            page.goto(ORDER_URL, timeout=30000, wait_until="networkidle")
            time.sleep(5)
            print("[OK] 页面加载完成")
            
            # 定位到 Frame 5 (biddermsg)
            print("\n[3] 定位 iframe...")
            target_frame = None
            
            # 通过 URL 特征查找正确的 frame
            for frame in page.frames:
                if 'biddermsg' in frame.url or 'order' in frame.url.lower():
                    print(f"[OK] 找到目标 frame: {frame.url[:150]}")
                    target_frame = frame
                    break
            
            if not target_frame and len(page.frames) > 5:
                target_frame = page.frames[5]
                print(f"[INFO] 使用 Frame 5: {target_frame.url[:150]}")
            
            if not target_frame:
                print("[ERROR] 未找到目标 frame")
                return
            
            # 在 frame 中查找订单数据
            print("\n[4] 获取订单数据...")
            
            # 等待更长时间让动态内容加载
            time.sleep(5)
            
            # 查找所有包含文本的元素
            print("[INFO] 查找订单列表...")
            
            # 尝试多种选择器
            selectors = [
                'tbody tr',
                '.ant-table-row',
                '.el-table__row',
                '[class*="row"]',
                'div[class*="list"] > div',
                '[class*="order"]',
            ]
            
            all_rows = []
            for sel in selectors:
                try:
                    rows = target_frame.query_selector_all(sel)
                    if rows:
                        print(f"  选择器 '{sel}': {len(rows)} 行")
                        all_rows.extend(rows)
                except:
                    continue
            
            print(f"[INFO] 共找到 {len(all_rows)} 行")
            
            # 保存 frame 的 HTML
            html_path = "output/frame_content.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(target_frame.content())
            print(f"[OK] 已保存 frame HTML: {html_path}")
            
            # 获取整个页面的文本内容
            print("\n[5] 提取文本内容...")
            try:
                page_text = target_frame.inner_text('body', timeout=10000)
                text_path = "output/frame_text.txt"
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(page_text)
                print(f"[OK] 已保存文本：{text_path}")
                
                # 查找包含日期的行
                lines = page_text.split('\n')
                print(f"[INFO] 共 {len(lines)} 行文本")
                
                current_order = {}
                for i, line in enumerate(lines[:500]):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查是否是 3 月份订单
                    if '2026-03-' in line or '2026/03/' in line or '2026 年 03 月' in line or '26 年 03 月' in line:
                        print(f"\n[订单] 找到 3 月订单 (行{i}):")
                        print(f"  {line[:200]}")
                        
                        # 向前后查找相关信息
                        context_start = max(0, i-5)
                        context_end = min(len(lines), i+10)
                        context = '\n'.join([lines[j].strip() for j in range(context_start, context_end) if lines[j].strip()])
                        
                        order_info = {
                            'line': i,
                            'content': line,
                            'context': context,
                            'captured_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        orders_data.append(order_info)
                
            except Exception as e:
                print(f"[WARN] 提取文本失败：{e}")
            
            print(f"\n[OK] 共获取 {len(orders_data)} 条 3 月份订单")
            
            # 保存
            print("\n[6] 保存数据...")
            json_path = "output/orders_202603_v4.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] JSON: {json_path}")
            
            # 打印
            print("\n" + "=" * 80)
            print("[订单摘要]")
            print("=" * 80)
            for i, order in enumerate(orders_data[:20]):
                print(f"\n{i+1}. 行{order['line']}: {order['content'][:150]}")
            
            print("\n" + "=" * 80)
            print(f"[DONE] 完成 - 共{len(orders_data)}条订单")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            browser.close()
    
    return orders_data


if __name__ == '__main__':
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    get_orders()
