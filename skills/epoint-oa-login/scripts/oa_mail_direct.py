# -*- utf-8 -*-
"""
直接使用已保存的 Cookie 登录 OA 并获取邮件列表
"""
import sys
import os
import time
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_HOME_URL = "https://oa.epoint.com.cn/wboa9/"

def get_mail_list():
    playwright = None
    context = None
    
    try:
        print("=" * 60)
        print("OA 邮件列表获取工具")
        print("=" * 60)
        print("\n👉 使用已保存的 Cookie 登录...")
        
        playwright = sync_playwright().start()
        
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.new_page()
        
        # 访问 OA 首页
        print(f"👉 访问 OA 首页：{OA_HOME_URL}")
        page.goto(OA_HOME_URL, wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        current_url = page.url
        print(f"\n📊 当前 URL: {current_url}")
        print(f"📊 页面标题：{page.title()}")
        
        # 检查是否登录
        if 'login' in current_url.lower():
            print("\n❌ Cookie 已过期，需要重新登录")
            return
        
        print("\n✅ 登录成功！")
        
        # 查找邮件入口
        print("\n👉 查找邮件入口...")
        
        # 尝试多种选择器查找邮件链接/按钮
        selectors = [
            'a[href*="mail"]',
            'a:has-text("邮件")',
            'a:has-text("公务邮件")',
            '[title*="邮件"]',
            '[alt*="邮件"]',
            'img[src*="mail"]',
        ]
        
        mail_link = None
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"  选择器 '{selector}' 找到 {len(elements)} 个元素")
                    for el in elements:
                        try:
                            text = el.inner_text(timeout=1000)
                            href = el.get_attribute('href', timeout=1000)
                            if text or href:
                                print(f"    - 文本：{text[:30]}, href: {href[:50] if href else 'N/A'}")
                                if 'mail' in (text + (href or '')).lower() or '邮件' in text:
                                    mail_link = el
                                    break
                        except:
                            pass
                    if mail_link:
                        break
            except Exception as e:
                print(f"  选择器 '{selector}' 失败：{e}")
        
        if mail_link:
            print("\n👉 点击邮件入口...")
            try:
                # 获取点击后的 URL
                with page.expect_navigation(timeout=10000) as nav_info:
                    mail_link.click(timeout=5000)
                print(f"✅ 已跳转到：{page.url}")
                time.sleep(3)
            except Exception as e:
                print(f"点击失败：{e}")
                print("💡 请手动在浏览器中点击邮件按钮")
        else:
            print("\n⚠️ 未找到邮件入口，请手动在浏览器中点击")
        
        # 获取页面内容
        print("\n📊 当前页面信息:")
        print(f"   URL: {page.url}")
        print(f"   标题：{page.title()}")
        
        # 保存页面
        html = page.content()
        with open('oa_mail_page.html', 'w', encoding='utf-8') as f:
            f.write(html[:100000])
        print("\n📄 已保存：oa_mail_page.html")
        
        page.screenshot(path='oa_mail_page.png', full_page=True)
        print("📸 已保存：oa_mail_page.png")
        
        # 尝试查找邮件列表
        print("\n📧 尝试获取邮件列表...")
        bodies = page.query_selector_all('body')
        if bodies:
            text = bodies[0].inner_text(timeout=5000)
            lines = [line.strip() for line in text.split('\n') if line.strip()][:30]
            print("页面文本前 30 行:")
            for line in lines:
                print(f"  {line[:100]}")
        
        print("\n✅ 浏览器保持打开")
        print("   按回车键退出...")
        input()
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if context:
            context.close()
        if playwright:
            playwright.stop()

if __name__ == '__main__':
    get_mail_list()
