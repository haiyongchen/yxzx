from browser_manager import get_page


# ✅ 通用等待函数（解决跳转问题）
def wait_for_oa_ready(page):
    try:
        # 等进入业务系统
        page.wait_for_url("**/wboa9/**", timeout=30000)
    except:
        pass

    # 等页面基本稳定
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except:
        pass

    # 再保险等一下（防 iframe / JS 渲染）
    page.wait_for_timeout(2000)


# ✅ 获取主frame（解决 iframe 问题）
def get_main_frame(page):
    # 常见 iframe（OA系统大概率用）
    frames = page.frames

    for f in frames:
        if "wboa9" in f.url or f != page.main_frame:
            return f

    return page.main_frame


# ✅ 工具1：打开OA首页
def open_oa_home():
    page = get_page()

    page.goto("https://oa.epoint.com.cn/wboa9/")

    wait_for_oa_ready(page)

    return {
        "status": "success",
        "url": page.url
    }


# ✅ 工具2：获取标题（已修复报错）
def get_page_title():
    page = get_page()

    wait_for_oa_ready(page)

    # 防止 context 销毁
    for _ in range(3):
        try:
            return {"title": page.title()}
        except:
            page.wait_for_timeout(1000)

    return {"error": "获取标题失败"}


# ✅ 工具3：获取页面文本（支持 iframe）
def get_page_text():
    page = get_page()

    wait_for_oa_ready(page)

    frame = get_main_frame(page)

    for _ in range(3):
        try:
            text = frame.locator("body").inner_text(timeout=5000)
            return {"content": text[:2000]}
        except:
            page.wait_for_timeout(1000)

    return {"error": "获取内容失败"}


# ✅ 工具4：点击菜单（更稳版本）
def click_menu(menu_name: str):
    page = get_page()

    page.goto("https://oa.epoint.com.cn/wboa9/")
    wait_for_oa_ready(page)

    frame = get_main_frame(page)

    try:
        frame.locator(f"text={menu_name}").first.click(timeout=5000)
        return {
            "status": "clicked",
            "menu": menu_name
        }
    except:
        return {
            "error": f"未找到菜单: {menu_name}"
        }


# ✅ 工具5：调试用（看所有frame）
def debug_frames():
    page = get_page()

    frames_info = []
    for f in page.frames:
        frames_info.append(f.url)

    return {"frames": frames_info}