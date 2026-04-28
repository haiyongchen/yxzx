from playwright.sync_api import sync_playwright

user_data_dir = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    
    # 获取未读邮件
    page = browser.new_page()
    page.goto("https://oa.epoint.com.cn/wboa9/mail_getunreadlist.action")
    page.wait_for_load_state("networkidle")
    
    print("=== 页面标题 ===")
    print(page.title())
    print("\n=== 页面URL ===")
    print(page.url)
    
    # 尝试获取未读邮件数量
    try:
        # 尝试获取表格行
        rows = page.locator("table tr, .mail-list li, .unread-item").count()
        print(f"\n=== 未读邮件数量: {rows} ===")
    except:
        pass
    
    # 打印页面内容片段
    content = page.content()
    import re
    # 查找数字
    numbers = re.findall(r'\d+', content[:3000])
    print(f"\n=== 页面数字: {numbers[:20]} ===")
    
    input("\n按回车键关闭浏览器...")
    browser.close()
