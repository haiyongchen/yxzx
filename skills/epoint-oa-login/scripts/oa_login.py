# -*- coding: utf-8 -*-
"""
新点 OA 系统自动登录脚本
支持自动登录、状态检测、扫码更新
"""
import argparse
import sys
import os

# 设置 stdout 编码为 utf-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加父目录到路径以导入 skill 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epoint_oa_login import open_oa, open_oa_url, check_login_status, refresh_login


def main():
    parser = argparse.ArgumentParser(description='新点 OA 系统自动登录工具')
    parser.add_argument('--url', '-u', help='指定要打开的 URL')
    parser.add_argument('--refresh', '-r', action='store_true', help='刷新登录状态（扫码登录）')
    parser.add_argument('--check', '-c', action='store_true', help='检查登录状态')
    parser.add_argument('--headless', action='store_true', help='无头模式（不显示浏览器窗口）')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("新点 OA 系统自动登录工具")
    print("=" * 60)
    
    if args.check:
        print("\n👉 正在检查登录状态...")
        result = check_login_status(headless=args.headless)
        if result.get('logged_in'):
            print(f"✅ 登录状态有效")
            print(f"   URL: {result.get('url')}")
            print(f"   标题: {result.get('title')}")
        else:
            print(f"❌ 登录状态已过期")
            print(f"   提示: 使用 --refresh 参数重新登录")
        return 0 if result.get('logged_in') else 1
    
    elif args.refresh:
        print("\n👉 正在刷新登录状态...")
        print("   将弹出浏览器窗口，请扫码登录")
        result = refresh_login()
        if result.get('status') == 'success':
            print(f"✅ {result.get('message')}")
            return 0
        else:
            print(f"❌ {result.get('message')}")
            return 1
    
    elif args.url:
        print(f"\n👉 正在打开: {args.url}")
        result = open_oa_url(args.url, headless=args.headless)
        if result.get('status') == 'success':
            print(f"✅ 打开成功")
            print(f"   URL: {result.get('url')}")
            print(f"   标题: {result.get('title')}")
            return 0
        elif result.get('status') == 'login_required':
            print(f"⚠️ {result.get('message')}")
            print(f"   请使用 --refresh 参数重新登录")
            return 1
        else:
            print(f"❌ 打开失败: {result.get('message')}")
            return 1
    
    else:
        # 默认打开 OA 首页
        print("\n👉 正在打开 OA 首页...")
        result = open_oa(headless=args.headless)
        if result.get('status') == 'success':
            print(f"✅ 登录成功")
            print(f"   URL: {result.get('url')}")
            print(f"   标题: {result.get('title')}")
            return 0
        elif result.get('status') == 'login_required':
            print(f"⚠️ {result.get('message')}")
            print(f"   请使用 --refresh 参数重新登录")
            return 1
        else:
            print(f"❌ 登录失败: {result.get('message')}")
            return 1


if __name__ == '__main__':
    sys.exit(main())
