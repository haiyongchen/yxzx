#!/usr/bin/env python3
"""
使用 Playwright 加载 cookies 并导出 e交易数据 - 简化版
"""

import asyncio
import json
from playwright.async_api import async_playwright

def convert_cookie(cookie):
    """转换 cookie 格式以兼容 Playwright"""
    same_site = cookie.get("sameSite", "unspecified")
    if same_site == "unspecified":
        same_site = "None"
    
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
        # 启动新浏览器
        browser = await p.chromium.launch(headless=False)
        
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
        
        # 创建新页面
        print("导航到目标页面...")
        page = await context.new_page()
        
        # 导航到目标页面，增加超时时间
        try:
            await page.goto(
                "https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist",
                timeout=60000,
                wait_until="domcontentloaded"
            )
        except Exception as e:
            print(f"页面加载超时，但继续执行: {e}")
        
        await asyncio.sleep(10)
        
        print(f"当前页面: {page.url}")
        
        # 截图查看页面状态
        await page.screenshot(path="D:\\openclaw-workspace\\epoint_page.png")
        print("已保存截图: epoint_page.png")
        
        # 获取页面内容
        content = await page.content()
        print(f"页面内容长度: {len(content)}")
        
        # 查找"导出"相关按钮
        buttons = await page.query_selector_all('button')
        print(f"找到 {len(buttons)} 个按钮")
        
        for i, btn in enumerate(buttons[:10]):  # 只查看前10个
            try:
                text = await btn.text_content()
                if text and "导出" in text:
                    print(f"  找到导出按钮 {i}: {text}")
                    await btn.click()
                    print(f"  已点击")
                    await asyncio.sleep(3)
            except:
                pass
        
        await asyncio.sleep(5)
        
        # 截图查看结果
        await page.screenshot(path="D:\\openclaw-workspace\\epoint_after.png")
        print("已保存截图: epoint_after.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(export_data())
