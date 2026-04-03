# -*- coding: utf-8 -*-
"""
新点 OA 系统自动登录模块
"""
from playwright.sync_api import sync_playwright
import time
import os

# 用户数据目录
USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"

# OA 系统 URL
OA_HOME_URL = "https://oa.epoint.com.cn/wboa9/"


def _launch_browser(headless=False, channel="chrome"):
    """启动浏览器并返回上下文和页面"""
    playwright = sync_playwright().start()
    
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel=channel,
        headless=headless,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    )
    
    page = context.new_page()
    return playwright, context, page


def _is_logged_in(page):
    """检查是否已登录"""
    current_url = page.url
    title = page.title()
    
    # 如果 URL 包含 login 或 oauth2login，说明需要登录
    if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
        return False
    
    # 如果标题包含"登录"，说明需要登录
    if '登录' in title:
        return False
    
    return True


def check_login_status(headless=True):
    """
    检查当前登录状态
    
    Returns:
        dict: {'logged_in': bool, 'url': str, 'title': str}
    """
    try:
        playwright, context, page = _launch_browser(headless=headless)
        
        # 访问 OA 首页
        page.goto(OA_HOME_URL)
        time.sleep(3)
        
        logged_in = _is_logged_in(page)
        result = {
            'logged_in': logged_in,
            'url': page.url,
            'title': page.title()
        }
        
        context.close()
        playwright.stop()
        
        return result
        
    except Exception as e:
        return {
            'logged_in': False,
            'error': str(e)
        }


def refresh_login(channel="chrome"):
    """
    刷新登录状态（扫码登录）
    
    Returns:
        dict: {'status': 'success'/'error', 'message': str}
    """
    try:
        print("👉 正在启动浏览器...")
        playwright, context, page = _launch_browser(headless=False, channel=channel)
        
        # 访问 OA 首页
        print("👉 正在访问 OA 系统...")
        page.goto(OA_HOME_URL)
        time.sleep(2)
        
        # 检查是否需要登录
        if _is_logged_in(page):
            print("✅ 登录状态有效，无需重新登录")
            # 保持运行一段时间确保状态保存
            time.sleep(5)
            context.close()
            playwright.stop()
            return {
                'status': 'success',
                'message': '登录状态有效，无需重新登录'
            }
        
        # 需要登录
        print("\n⚠️ 需要登录")
        print("👉 请在浏览器窗口中扫码登录")
        print("👉 登录完成后，按回车键继续...")
        
        input()
        
        # 等待页面稳定
        time.sleep(3)
        
        if _is_logged_in(page):
            print("✅ 登录成功！正在保存状态...")
            # 保持运行一段时间确保状态保存到磁盘
            time.sleep(10)
            context.close()
            playwright.stop()
            return {
                'status': 'success',
                'message': '登录状态已更新并保存'
            }
        else:
            context.close()
            playwright.stop()
            return {
                'status': 'error',
                'message': '登录未完成或失败'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'刷新登录状态失败: {str(e)}'
        }


def open_oa(headless=False, channel="chrome"):
    """
    自动登录 OA 系统并打开首页
    
    Args:
        headless: 是否使用无头模式
        channel: 浏览器通道 (chrome/edge)
    
    Returns:
        dict: {'status': 'success'/'login_required'/'error', ...}
    """
    try:
        playwright, context, page = _launch_browser(headless=headless, channel=channel)
        
        # 访问 OA 首页
        page.goto(OA_HOME_URL)
        time.sleep(3)
        
        # 检查是否已登录
        if not _is_logged_in(page):
            context.close()
            playwright.stop()
            return {
                'status': 'login_required',
                'message': '登录状态已过期，需要重新扫码登录',
                'url': page.url,
                'title': page.title()
            }
        
        # 已登录，保持浏览器运行一段时间
        result = {
            'status': 'success',
            'url': page.url,
            'title': page.title()
        }
        
        # 如果不是无头模式，保持运行让用户看到
        if not headless:
            time.sleep(5)
        
        context.close()
        playwright.stop()
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


def open_oa_url(url, headless=False, channel="chrome"):
    """
    使用已保存的登录状态打开指定的 OA 子系统 URL
    
    Args:
        url: 目标 URL
        headless: 是否使用无头模式
        channel: 浏览器通道 (chrome/edge)
    
    Returns:
        dict: {'status': 'success'/'login_required'/'error', ...}
    """
    try:
        playwright, context, page = _launch_browser(headless=headless, channel=channel)
        
        # 访问指定 URL
        page.goto(url)
        time.sleep(3)
        
        # 检查是否跳转到登录页
        current_url = page.url
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            context.close()
            playwright.stop()
            return {
                'status': 'login_required',
                'message': '登录状态已过期，需要重新扫码登录',
                'url': current_url,
                'title': page.title()
            }
        
        # 成功打开
        result = {
            'status': 'success',
            'url': page.url,
            'title': page.title()
        }
        
        # 如果不是无头模式，保持运行让用户看到
        if not headless:
            time.sleep(5)
        
        context.close()
        playwright.stop()
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


def get_page_content(url=None, headless=True):
    """
    获取 OA 页面内容
    
    Args:
        url: 目标 URL，默认为 OA 首页
        headless: 是否使用无头模式
    
    Returns:
        dict: {'status': 'success'/'error', 'content': str, ...}
    """
    try:
        target_url = url or OA_HOME_URL
        playwright, context, page = _launch_browser(headless=headless)
        
        page.goto(target_url)
        time.sleep(3)
        
        if not _is_logged_in(page):
            context.close()
            playwright.stop()
            return {
                'status': 'login_required',
                'message': '登录状态已过期'
            }
        
        # 获取页面文本内容
        content = page.locator("body").inner_text(timeout=5000)
        
        context.close()
        playwright.stop()
        
        return {
            'status': 'success',
            'content': content[:2000],  # 限制返回长度
            'url': page.url,
            'title': page.title()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
