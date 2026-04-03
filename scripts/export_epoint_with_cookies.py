#!/usr/bin/env python3
"""
使用 Playwright 加载 cookies 并导出 e交易数据
"""

import asyncio
import json
from playwright.async_api import async_playwright

def convert_cookie(cookie):
    """转换 cookie 格式以兼容 Playwright"""
    # 转换 sameSite 值
    same_site = cookie.get("sameSite", "unspecified")
    if same_site == "unspecified":
        same_site = "None"
    
    # 转换 expirationDate 为 expires (秒)
    expires = -1
    if "expirationDate" in cookie:
        expires = int(cookie["expirationDate"])
    
    return {
        "name": cookie["name"],
        "value": cookie["value"],
        "domain": cookie["domain"],
        "path": cookie["path"],
        "expires": expires,
        "httpOnly": cookie.get("httpOnly", False),
        "secure": cookie.get("secure", False),
        "sameSite": same_site
    }

async def export_data():
    async with async_playwright() as p:
        # 连接到 browser relay 的 CDP
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        
        # 创建新上下文并加载 cookies
        context = await browser.new_context()
        
        # 读取 cookies
        with open("epoint_cookies.json", "r", encoding="utf-8") as f:
            cookies_raw = json.load(f)
        
        # 转换 cookies 格式
        cookies = [convert_cookie(c) for c in cookies_raw]
        
        # 添加 cookies 到上下文
        await context.add_cookies(cookies)
        print(f"已加载 {len(cookies)} 个 cookies")
        
        # 创建新页面并导航到目标网址
        print("导航到目标页面...")
        page = await context.new_page()
        await page.goto("https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist")
        await asyncio.sleep(5)
        
        print(f"当前页面: {page.url}")
        
        # 截图查看页面状态
        await page.screenshot(path="D:\\openclaw-workspace\\epoint_page.png")
        print("已保存截图: epoint_page.png")
        
        # 等待页面加载完成
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        
        # 尝试找到并操作"默认 3"选项
        try:
            # 尝试多种方式找到"默认"相关的元素
            # 方法1: 通过文本查找
            default_elements = await page.query_selector_all('text=/默认/')
            print(f"找到 {len(default_elements)} 个包含'默认'文本的元素")
            
            for i, elem in enumerate(default_elements):
                try:
                    text = await elem.text_content()
                    print(f"  元素 {i}: {text}")
                    
                    # 如果是复选框或包含复选框，尝试点击
                    checkbox = await elem.query_selector('input[type="checkbox"]')
                    if checkbox:
                        is_checked = await checkbox.is_checked()
                        print(f"    复选框状态: {'已选中' if is_checked else '未选中'}")
                        if is_checked:
                            await checkbox.click()
                            print(f"    已取消选中")
                    else:
                        # 尝试直接点击元素
                        await elem.click()
                        print(f"    已点击元素")
                except Exception as e:
                    print(f"    操作元素时出错: {e}")
        except Exception as e:
            print(f"查找'默认'选项时出错: {e}")
        
        await asyncio.sleep(2)
        
        # 尝试点击"导出平台数据"按钮
        try:
            # 方法1: 通过文本查找按钮
            export_button = await page.query_selector('button:has-text("导出平台数据")')
            if export_button:
                print("找到'导出平台数据'按钮（方法1）")
                await export_button.click()
                print("已点击导出按钮")
            else:
                # 方法2: 通过部分文本查找
                export_button = await page.query_selector('text="导出"')
                if export_button:
                    print("找到包含'导出'文本的按钮（方法2）")
                    await export_button.click()
                    print("已点击导出按钮")
                else:
                    print("未找到导出按钮")
            
            # 等待下载
            await asyncio.sleep(5)
            
            # 截图查看结果
            await page.screenshot(path="D:\\openclaw-workspace\\epoint_after_export.png")
            print("已保存截图: epoint_after_export.png")
            
        except Exception as e:
            print(f"点击导出按钮时出错: {e}")
        
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(export_data())
