# -*- coding: utf-8 -*-
"""
OA 邮件监控脚本 - 点击邮件按钮并监控网络请求
"""
import sys
import os
import time
import json

# 设置 stdout 编码为 utf-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

# 用户数据目录
USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"

# OA 系统 URL
OA_HOME_URL = "https://oa.epoint.com.cn/wboa9/"


def monitor_mail_requests():
    """
    打开 OA 页面，点击邮件按钮，监控网络请求
    """
    print("=" * 60)
    print("OA 邮件监控工具")
    print("=" * 60)
    
    playwright = None
    context = None
    page = None
    
    try:
        print("\n👉 启动浏览器...")
        playwright = sync_playwright().start()
        
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        page = context.new_page()
        
        # 设置网络请求监控
        print("👉 设置网络请求监控...")
        requests_log = []
        
        def handle_request(request):
            url = request.url
            # 只记录邮件相关的请求
            if any(keyword in url.lower() for keyword in ['mail', 'email', 'message', 'inbox']):
                requests_log.append({
                    'url': url,
                    'method': request.method,
                    'resource_type': request.resource_type,
                    'time': time.time()
                })
                print(f"📧 捕获邮件请求：{request.method} {url[:150]}")
        
        page.on('request', handle_request)
        
        # 访问 OA 首页
        print(f"\n👉 访问 OA 首页：{OA_HOME_URL}")
        page.goto(OA_HOME_URL, wait_until='networkidle')
        time.sleep(3)
        
        # 检查是否已登录
        current_url = page.url
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("⚠️ 未登录，请在浏览器窗口中扫码登录 OA 系统")
            print("👉 扫码登录完成后，按回车键继续...")
            input()
            time.sleep(3)
            # 重新检查登录状态
            current_url = page.url
            if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
                print("❌ 登录未完成，退出")
                return
            print("✅ 登录成功！")
        
        print("✅ 已登录 OA 系统")
        print(f"当前页面：{page.title()}")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 查找并点击邮件按钮
        print("\n👉 查找邮件按钮...")
        
        # 尝试多种选择器
        mail_selectors = [
            'img[alt="邮件"]',
            'img[src*="mail"]',
            '.mail-icon',
            '[title*="邮件"]',
            'text=邮件',
        ]
        
        mail_clicked = False
        
        # 先尝试截图识别
        print("📸 截取当前页面...")
        page.screenshot(path='oa_home_screenshot.png')
        print("截图已保存：oa_home_screenshot.png")
        
        # 获取页面 HTML 结构来分析
        print("\n👉 分析页面结构...")
        html_content = page.content()
        
        # 查找包含"邮件"的元素
        mail_elements = page.query_selector_all('text=邮件')
        print(f"找到 {len(mail_elements)} 个包含'邮件'的元素")
        
        if mail_elements:
            # 尝试点击第一个邮件元素
            for i, element in enumerate(mail_elements):
                try:
                    element_text = element.inner_text(timeout=2000)
                    print(f"  元素 {i}: {element_text[:50]}")
                    
                    # 检查是否是可点击的元素
                    if element.is_visible() and element.is_enabled():
                        print(f"\n👉 点击邮件元素 (索引 {i})...")
                        element.click(timeout=5000)
                        mail_clicked = True
                        break
                except Exception as e:
                    print(f"  元素 {i} 点击失败：{e}")
                    continue
        
        # 如果没找到，尝试使用图像识别或坐标点击
        if not mail_clicked:
            print("\n⚠️ 未找到邮件按钮，尝试其他方式...")
            
            # 尝试点击红色邮件图标区域（根据截图中的位置）
            # 这需要手动调整坐标
            print("💡 提示：请手动点击浏览器中的红色邮件按钮")
            print("   点击后我会监控网络请求...")
            
            # 等待用户手动操作
            time.sleep(5)
        
        # 等待网络请求
        print("\n👉 等待网络请求 (10 秒)...")
        for i in range(10):
            time.sleep(1)
            print(f"   等待中... {i+1}/10")
        
        # 获取当前页面内容
        print("\n👉 获取当前页面信息...")
        print(f"当前 URL: {page.url}")
        print(f"页面标题：{page.title()}")
        
        # 尝试获取邮件列表内容
        try:
            # 查找邮件列表元素
            mail_list = page.query_selector_all('.mail-item, .email-item, [class*="mail"], [class*="email"]')
            print(f"\n📧 找到 {len(mail_list)} 个邮件相关元素")
            
            for i, item in enumerate(mail_list[:5]):  # 只显示前 5 个
                try:
                    text = item.inner_text(timeout=2000)
                    if text.strip():
                        print(f"  邮件 {i+1}: {text[:100]}")
                except:
                    pass
        except Exception as e:
            print(f"获取邮件列表失败：{e}")
        
        # 输出捕获的请求
        print(f"\n📊 共捕获 {len(requests_log)} 个邮件相关请求:")
        for req in requests_log:
            print(f"  {req['method']} {req['url'][:100]}")
        
        # 保存页面截图
        page.screenshot(path='oa_mail_screenshot.png')
        print("\n📸 最终页面截图：oa_mail_screenshot.png")
        
        # 保持浏览器打开，让用户继续操作
        print("\n✅ 浏览器保持打开状态")
        print("   你可以在浏览器中继续操作邮件功能")
        print("   按回车键退出...")
        input()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if context:
            context.close()
        if playwright:
            playwright.stop()


if __name__ == '__main__':
    monitor_mail_requests()
