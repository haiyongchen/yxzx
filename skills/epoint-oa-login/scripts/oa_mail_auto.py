# -*- utf-8 -*-
"""
OA 自动化邮件工具 - 完全自动化操作
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

def automate_mail():
    playwright = None
    context = None
    
    try:
        print("=" * 60)
        print("OA 自动化邮件工具")
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
        time.sleep(3)
        
        current_url = page.url
        
        # 检查是否需要登录
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("\n⚠️  需要扫码登录")
            print("👉 请在浏览器窗口中使用 OA App 扫码")
            print("👉 扫码完成后按回车键继续...")
            input()
            time.sleep(3)
            
            print("\n👉 等待页面跳转...")
            try:
                with page.expect_navigation(timeout=15000):
                    pass
            except:
                pass
            time.sleep(2)
        
        print("\n✅ 登录成功！")
        print(f"   当前 URL: {page.url}")
        print(f"   页面标题：{page.title()}")
        
        # 自动查找并点击邮件入口
        # 直接使用解析出的邮件 URL
        MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"
        print(f"\n👉 直接访问邮件页面：{MAIL_URL}")
        
        page.goto(MAIL_URL, wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        print("\n✅ 已打开邮件页面")
        
        # 获取当前页面信息
        print("\n📊 当前页面信息:")
        print(f"   URL: {page.url}")
        print(f"   标题：{page.title()}")
        
        # 保存截图
        page.screenshot(path='oa_mail_page.png', full_page=True)
        print("\n📸 已保存页面截图：oa_mail_page.png")
        
        # 尝试获取邮件列表内容
        print("\n📧 获取邮件列表内容...")
        try:
            text = page.locator("body").inner_text(timeout=5000)
            lines = [line.strip() for line in text.split('\n') if line.strip()][:100]
            print("\n📄 页面文本内容 (前 100 行):")
            for i, line in enumerate(lines[:50]):
                print(f"  [{i+1}] {line[:120]}")
        except Exception as e:
            print(f"获取页面内容失败：{e}")
        
        # 保存 HTML
        html = page.content()
        with open('oa_mail_page.html', 'w', encoding='utf-8') as f:
            f.write(html[:100000])
        print("\n📄 已保存 HTML: oa_mail_page.html")
        
        print("\n✅ 自动化完成！")
        print("   浏览器保持打开，可在其中继续操作")
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
    automate_mail()
