# -*- coding: utf-8 -*-
"""
系统登录测试脚本
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from datetime import datetime
import sys

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 系统配置
SYSTEM_URL = "https://dev-ec.cneptp.com:10081/epoint-sso_cs/default/login"
USERNAME = "admin"
PASSWORD = "Epoint@123456"

def login_and_test():
    """登录系统并测试"""
    print("=" * 60)
    print("[TEST] 系统登录测试")
    print("=" * 60)
    print(f"系统地址：{SYSTEM_URL}")
    print(f"登录账号：{USERNAME}")
    print(f"登录时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 启动浏览器
        print("[INFO] 启动浏览器...")
        browser = p.chromium.launch(headless=False, slow_mo=500)
        
        # 创建上下文
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 创建页面
        page = context.new_page()
        
        try:
            # 访问登录页
            print(f"[INFO] 访问登录页面：{SYSTEM_URL}")
            page.goto(SYSTEM_URL, timeout=30000, wait_until="networkidle")
            print("[OK] 页面加载完成")
            
            # 截图保存
            screenshot_path = "output/login_page.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存截图：{screenshot_path}")
            
            # 等待页面稳定
            time.sleep(2)
            
            # 尝试自动登录
            print("\n[INFO] 尝试自动登录...")
            
            # 常见的登录表单选择器
            login_selectors = [
                'input[type="text"]',
                'input[name="username"]',
                'input[id="username"]',
                'input[placeholder*="账号"]',
                'input[placeholder*="用户名"]',
                'input[placeholder*="account"]',
            ]
            
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id="password"]',
                'input[placeholder*="密码"]',
                'input[placeholder*="password"]',
            ]
            
            button_selectors = [
                'button[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Login")',
                'input[type="submit"]',
                '.login-btn',
                '#loginBtn',
                'button[class*="login"]',
            ]
            
            # 查找用户名输入框
            username_input = None
            for selector in login_selectors:
                try:
                    username_input = page.query_selector(selector)
                    if username_input:
                        print(f"[OK] 找到用户名输入框：{selector}")
                        break
                except:
                    continue
            
            # 查找密码输入框
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = page.query_selector(selector)
                    if password_input:
                        print(f"[OK] 找到密码输入框：{selector}")
                        break
                except:
                    continue
            
            # 查找登录按钮
            login_button = None
            for selector in button_selectors:
                try:
                    login_button = page.query_selector(selector)
                    if login_button:
                        print(f"[OK] 找到登录按钮：{selector}")
                        break
                except:
                    continue
            
            # 如果找到了表单元素，尝试登录
            if username_input and password_input and login_button:
                print("\n[INFO] 开始登录...")
                
                # 输入用户名
                username_input.fill(USERNAME)
                print(f"   已输入用户名：{USERNAME}")
                
                # 输入密码
                password_input.fill(PASSWORD)
                print(f"   已输入密码：{'*' * len(PASSWORD)}")
                
                # 等待一下
                time.sleep(1)
                
                # 点击登录按钮
                login_button.click()
                print("   已点击登录按钮")
                
                # 等待页面跳转
                print("\n[INFO] 等待登录完成...")
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                    print("[OK] 登录完成")
                    
                    # 截图保存登录后的页面
                    screenshot_path = "output/logged_in.png"
                    page.screenshot(path=screenshot_path, full_page=True)
                    print(f"[OK] 已保存登录后截图：{screenshot_path}")
                    
                    # 获取当前 URL
                    current_url = page.url
                    print(f"[INFO] 当前 URL: {current_url}")
                    
                    # 获取页面标题
                    page_title = page.title()
                    print(f"[INFO] 页面标题：{page_title}")
                    
                    # 检查是否登录成功（通过 URL 变化或页面内容）
                    if "login" not in current_url.lower():
                        print("\n[SUCCESS] 登录成功！URL 已变化")
                    else:
                        print("\n[WARN] URL 仍包含 login，可能登录未成功")
                    
                except PlaywrightTimeout:
                    print("[WARN] 登录等待超时，可能页面仍在加载")
                    
            else:
                print("\n[WARN] 未找到完整的登录表单元素")
                print(f"   用户名输入框：{'[OK]' if username_input else '[NOT FOUND]'}")
                print(f"   密码输入框：{'[OK]' if password_input else '[NOT FOUND]'}")
                print(f"   登录按钮：{'[OK]' if login_button else '[NOT FOUND]'}")
                
                # 列出页面上所有输入框
                print("\n[INFO] 页面上的输入框：")
                inputs = page.query_selector_all('input')
                for i, inp in enumerate(inputs[:15]):
                    try:
                        inp_type = inp.get_attribute('type')
                        inp_name = inp.get_attribute('name')
                        inp_id = inp.get_attribute('id')
                        inp_placeholder = inp.get_attribute('placeholder')
                        print(f"   {i+1}. type={inp_type}, name={inp_name}, id={inp_id}, placeholder={inp_placeholder}")
                    except:
                        continue
            
            print("\n" + "=" * 60)
            print("[DONE] 测试完成")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[ERROR] 测试失败：{e}")
            # 截图保存错误页面
            screenshot_path = "output/login_error.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[OK] 已保存错误页面截图：{screenshot_path}")
            
        finally:
            # 关闭浏览器
            print("\n[INFO] 关闭浏览器...")
            browser.close()
            print("[OK] 浏览器已关闭")


if __name__ == '__main__':
    # 确保输出目录存在
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)
    
    login_and_test()
