from playwright.sync_api import sync_playwright

playwright = None
context = None
page = None


def init_browser():
    global playwright, context, page

    if context is not None:
        return page

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir="oa_user_data",   # ⭐ 登录态核心
        channel="msedge",               # 用你本机 Edge
        headless=False,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = context.new_page()
    return page


def get_page():
    global page
    if page is None:
        page = init_browser()
    return page


def close_browser():
    """正确关闭浏览器并保存状态"""
    global playwright, context, page
    
    if page is not None:
        page.close()
        page = None
    
    if context is not None:
        context.close()
        context = None
    
    if playwright is not None:
        playwright.stop()
        playwright = None
    
    print("浏览器已关闭，登录状态已保存")