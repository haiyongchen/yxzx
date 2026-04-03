#!/usr/bin/env python3
"""
使用 Playwright 操作浏览器导出 e交易数据
"""

import asyncio
from playwright.async_api import async_playwright

async def export_data():
    async with async_playwright() as p:
        # 连接到 browser relay 的 CDP
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        
        # 获取所有页面
        contexts = browser.contexts
        if not contexts:
            print("没有找到浏览器上下文，创建新的")
            context = await browser.new_context()
        else:
            context = contexts[0]
        
        # 创建新页面并导航到目标网址
        print("创建新页面并导航到目标网址...")
        target_page = await context.new_page()
        await target_page.goto("https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist")
        await asyncio.sleep(5)
        
        print(f"当前页面: {target_page.url}")
        
        # 等待页面加载完成
        await target_page.wait_for_load_state("networkidle")
        
        # 查找并去掉"默认 3"的勾选
        # 先截图查看页面状态
        await target_page.screenshot(path="D:\\openclaw-workspace\\epoint_before.png")
        print("已保存截图: epoint_before.png")
        
        # 尝试找到搜索条件区域的"默认 3"选项
        # 由于无法直接看到页面结构，尝试常见的选择器
        try:
            # 尝试找到包含"默认"文本的元素
            default_checkbox = await target_page.query_selector('text="默认"')
            if default_checkbox:
                # 检查是否已选中
                is_checked = await default_checkbox.is_checked()
                if is_checked:
                    await default_checkbox.click()
                    print("已取消'默认'选项")
                else:
                    print("'默认'选项未选中")
            else:
                print("未找到'默认'选项")
        except Exception as e:
            print(f"操作'默认'选项时出错: {e}")
        
        # 尝试点击"导出平台数据"按钮
        try:
            # 尝试通过文本找到按钮
            export_button = await target_page.query_selector('text="导出平台数据"')
            if export_button:
                await export_button.click()
                print("已点击'导出平台数据'按钮")
                
                # 等待下载完成
                await asyncio.sleep(5)
                
                # 截图查看结果
                await target_page.screenshot(path="D:\\openclaw-workspace\\epoint_after.png")
                print("已保存截图: epoint_after.png")
            else:
                print("未找到'导出平台数据'按钮")
        except Exception as e:
            print(f"点击导出按钮时出错: {e}")
        
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(export_data())
