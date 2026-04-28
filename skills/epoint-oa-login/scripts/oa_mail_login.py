# -*- utf-8 -*-
"""
OA 登录并获取邮件列表 - 支持扫码登录
"""
import sys
import os
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_HOME_URL = "https://oa.epoint.com.cn/wboa9/"

def login_and_get_mail():
    playwright = None
    context = None
    
    try:
        print("=" * 60)
        print("OA 登录并获取邮件列表")
        print("=" * 60)
        
        playwright = sync_playwright().start()
        
        print("\n👉 启动浏览器...")
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.new_page()
        
        print(f"👉 访问 OA 首页：{OA_HOME_URL}")
        page.goto(OA_HOME_URL, wait_until='networkidle', timeout=30000)
        time.sleep(2)
        
        current_url = page.url
        
        # 检查是否需要登录
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("\n⚠️  需要扫码登录")
            print("👉 请在浏览器窗口中使用 OA App 扫码")
            print("👉 扫码完成后按回车键继续...")
            input()
            time.sleep(3)
            
            # 等待跳转到首页
            print("\n👉 等待页面跳转...")
            try:
                with page.expect_navigation(timeout=15000):
                    pass
            except:
                pass
            time.sleep(2)
            
            current_url = page.url
            if 'login' in current_url.lower():
                print("\n❌ 登录未完成，退出")
                return
        
        print("\n✅ 登录成功！")
        print(f"   当前 URL: {page.url}")
        print(f"   页面标题：{page.title()}")
        
        # 查找邮件入口
        print("\n👉 查找邮件入口...")
        time.sleep(2)
        
        # 截图看看页面布局
        page.screenshot(path='oa_home.png')
        print("📸 已保存首页截图：oa_home.png")
        
        # 尝试点击邮件图标
        mail_selectors = [
            'a[href*="mail"]',
            'a:has-text("邮件")',
            'a:has-text("公务邮件")',
            '[title*="邮件"]',
            'img[alt*="邮件"]',
        ]
        
        for selector in mail_selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"\n  找到 {len(elements)} 个匹配元素：{selector}")
                    for i, el in enumerate(elements[:3]):
                        try:
                            text = el.inner_text(timeout=1000)
                            print(f"    [{i}] {text[:50]}")
                        except:
                            pass
            except Exception as e:
                pass
        
        print("\n✅ 浏览器保持打开")
        print("   请在浏览器中手动点击邮件图标")
        print("   点击后按回车键，我会获取邮件列表...")
        input()
        
        # 获取当前页面信息
        print("\n📊 当前页面:")
        print(f"   URL: {page.url}")
        print(f"   标题：{page.title()}")
        
        # 获取页面文本
        try:
            text = page.locator("body").inner_text(timeout=5000)
            lines = [line.strip() for line in text.split('\n') if line.strip()][:50]
            print("\n📄 页面内容前 50 行:")
            for line in lines:
                print(f"  {line[:120]}")
        except Exception as e:
            print(f"获取页面内容失败：{e}")
        
        # 保存截图
        page.screenshot(path='oa_mail.png', full_page=True)
        print("\n📸 已保存截图：oa_mail.png")
        
        print("\n✅ 完成！")
        print("   按回车键关闭浏览器...")
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
    login_and_get_mail()
