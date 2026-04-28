#!/usr/bin/env python3
import requests
import json
import os
import subprocess
import sys
import argparse

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
TOKEN_FILE = os.path.join(BASE_DIR, "access_token.txt")
LOGIN_SCRIPT = os.path.join(SCRIPT_DIR, "oalogin.py")

BASE_URL = "https://oa.epoint.com.cn/oaextend/rest"
SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"

# OAuth2 应用凭证
CLIENT_ID = "8b205e73-955a-4ac7-a7ab-53ece32f396c"


def read_token():
    """从文件读取 access_token"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("access_token="):
                    return line.split("=", 1)[1]
    return None


def save_token(access_token):
    """保存 access_token 到文件"""
    with open(TOKEN_FILE, "w") as f:
        f.write(f"access_token={access_token}\n")
    print("[Info] Token 已保存", file=sys.stderr)


def check_token(access_token):
    """调用 checktoken 接口验证 token 是否有效"""
    url = f"{SSO_BASE}/rest/oauth2/checktoken"
    data = {
        "checktype": "DTO",
        "access_token": access_token
    }
    try:
        resp = requests.post(url, data=data, timeout=10, verify=False)
        result = resp.json()
        if "error" in result:
            print(f"[Info] Token 鉴权失败: {result.get('error_description', result.get('error'))}", file=sys.stderr)
            return False, result
        return True, result
    except Exception as e:
        print(f"[Warning] Token 检查异常: {e}", file=sys.stderr)
        return False, None


def qr_login():
    """执行扫码登录"""
    print("[Info] 启动扫码登录流程...", file=sys.stderr)
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    subprocess.run([sys.executable, LOGIN_SCRIPT], check=True)
    return read_token()


def get_token(force_login=False):
    """获取有效 Token: 鉴权检查 → 扫码登录"""
    if force_login:
        return qr_login()

    # 读取本地 Token
    access_token = read_token()
    if not access_token:
        print("[Info] 未找到本地 Token，启动扫码登录...", file=sys.stderr)
        return qr_login()

    # 鉴权检查
    valid, result = check_token(access_token)
    if valid:
        return access_token

    # Token 失效，直接扫码登录
    print("[Info] Token 已失效，启动扫码登录...", file=sys.stderr)
    return qr_login()


def call_api(api_path, params_json, use_form=False):
    """调用 OA 接口的主逻辑"""
    if api_path.startswith("http"):
        url = api_path
    elif api_path.startswith("/"):
        url = f"{BASE_URL}{api_path}"
    else:
        url = f"{BASE_URL}/dynamicapi/{api_path}" if "/" not in api_path else f"{BASE_URL}/{api_path}"

    token = get_token()
    if not token:
        print("[Error] 未能获取有效的 access_token", file=sys.stderr)
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    try:
        payload = json.loads(params_json) if params_json else {}
    except ValueError:
        print(f"[Error] 参数解析失败，请确保传入的是正确的 JSON 字符串: {params_json}", file=sys.stderr)
        return

    def perform_request(current_token):
        headers["Authorization"] = f"Bearer {current_token}"
        if use_form:
            return requests.post(url, headers=headers, data=payload, timeout=20, verify=False)
        else:
            return requests.post(url, headers=headers, json=payload, timeout=20, verify=False)

    response = perform_request(token)

    # 401 兜底重试 (安全网)
    if response.status_code == 401:
        print("[Warning] 请求返回 401，强制重新获取 Token...", file=sys.stderr)
        new_token = get_token(force_login=True)
        if new_token:
            response = perform_request(new_token)

    # 统一输出
    sys.stdout.reconfigure(encoding='utf-8')
    print(response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OA API 调用工具")
    parser.add_argument("api", help="API 路径 (例如: mail_getunreadlist_v7)")
    parser.add_argument("params", nargs="?", default="{}", help="JSON 格式参数")
    parser.add_argument("--form", action="store_true", help="使用 application/x-www-form-urlencoded 格式发送")

    args = parser.parse_args()
    requests.packages.urllib3.disable_warnings()
    call_api(args.api, args.params, args.form)
