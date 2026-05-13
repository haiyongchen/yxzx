from oa_tools import open_oa_home, get_page_title, get_page_text, debug_frames

if __name__ == "__main__":
    print("👉 打开OA")
    print(open_oa_home())

    input("👉 第一次请扫码登录，然后回车继续...")

    print("\n👉 标题")
    print(get_page_title())

    print("\n👉 页面内容")
    print(get_page_text())

    print("\n👉 Frame结构（调试用）")
    print(debug_frames())