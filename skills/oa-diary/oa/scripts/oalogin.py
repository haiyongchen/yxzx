#!/usr/bin/env python3
"""
OA系统老版二维码登录 - 自动获取access_token
流程：生成二维码 → 轮询扫码 → 登录 → 获取access_token
"""
import json, requests, qrcode, os, time, sys, re, subprocess
from urllib.parse import urlencode, urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
TOKEN_FILE = os.path.join(BASE_DIR, "access_token.txt")

SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_BASE = "https://oa.epoint.com.cn/epointoa9"
QR_LOGIN_URL = "http://218.4.136.126:1443/epointoa9/H5/oatest/ejs.m7.mobileframe.oa/pages/scanLogin/scan_login.html"

# OAuth2 参数（从抓包获取）
CLIENT_ID = "8b205e73-955a-4ac7-a7ab-53ece32f396c"
REDIRECT_URI = f"{OA_BASE}/frame/pages/login/login"

requests.packages.urllib3.disable_warnings()

def new_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://oa.epoint.com.cn',
        'Referer': f'{SSO_BASE}/login/oauth2login',
    })
    return s

def get_oauth2_state(session):
    """访问OAuth2登录页，获取state参数和cookie"""
    url = f"{SSO_BASE}/rest/oauth2/authorize"
    params = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
    }
    resp = session.get(url, params=params, allow_redirects=True, timeout=10)
    # 从页面或重定向URL中提取state
    state_match = re.search(r'state=([a-f0-9\-]+)', resp.url)
    if state_match:
        return state_match.group(1)
    # 尝试从HTML中找
    state_match = re.search(r'"state"\s*:\s*"([^"]+)"', resp.text)
    if state_match:
        return state_match.group(1)
    return None

def create_qr(session):
    """生成二维码（通过OAuth2登录页面）"""
    # 先访问登录页面获取必要的cookie
    url = f"{SSO_BASE}/rest/login/epoa9ssologinaction/page_load"
    params = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'isCommondto': 'true',
    }
    resp = session.post(url, params=params, data='', timeout=10)

    # 使用mcerthtmlservice的createQR生成二维码
    api = f"{SSO_BASE}/rest/mcerthtmlservice/doAction"
    import base64
    now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    org = base64.b64encode(f"111@{now_str}".encode()).decode()
    request_body = {
        "action": "createQR",
        "request": {
            "qrcodetype": "1",
            "signatureobjects": [{"objid": "", "org": org, "desc": "扫码登陆", "signed": ""}]
        }
    }
    params_json = json.dumps(request_body, separators=(',', ':'))
    resp = session.post(api, files={'params': (None, params_json, 'application/json')}, timeout=10)
    data = resp.json()
    qrcodeid = data["custom"]["qrcodeid"]
    return qrcodeid

def poll_scan(session, code):
    """轮询扫码状态，使用老版qrloginquery接口"""
    url = f"{SSO_BASE}/rest/qrcode/qrloginquery"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        'code': code,
        'time': timestamp,
        'order': 'query',
    }
    resp = session.post(url, data=data, timeout=10)
    try:
        result = resp.json()
        return result
    except:
        return {"scanned": False, "invalid": False}

def do_login(session, code):
    """扫码成功后，调用login接口"""
    url = f"{SSO_BASE}/rest/qrcode/qrloginquery"
    data = {
        'code': code,
        'time': '',
        'order': 'login',
    }
    resp = session.post(url, data=data, timeout=10)
    result = resp.json()
    return result

def oauth2_login(session, token, state):
    """调用登录接口，获取OAuth2 code"""
    url = f"{SSO_BASE}/rest/login/loginaction/login"

    commonDto = json.dumps([{
        "id": "epointca1",
        "type": "epointca",
        "action": "epointcaValue",
        "dataOptions": "{CAType:195}",
        "mapClass": "com.epoint.usercontrol.EpointCa",
        "value": json.dumps({
            "sN": "", "cN": "", "publicKey": "", "ePublicKey": "",
            "deviceNum": "", "qZ": "", "dS": "",
            "orgData": f"111@{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
            "cK": "", "yXQ": ""
        })
    }, {
        "id": "_common_hidden_viewdata",
        "type": "hidden",
        "value": ""
    }])

    cmdParams = json.dumps({
        "EpStr6": token,
        "EpStr1": "qrcodelogin",
        "loadType": "3"
    })

    resp = session.post(url, data={
        'commonDto': commonDto,
        'cmdParams': cmdParams,
    }, timeout=10)

    result = resp.json()
    # 从返回中获取OAuth2 authorize URL
    if result.get('status', {}).get('code') == '307':
        redirect_url = result['status']['url']
        return redirect_url
    return None

def get_access_token(session, oauth2_url, state):
    """通过OAuth2授权获取access_token"""
    full_url = f"{SSO_BASE}/{oauth2_url}"

    # 第一步：OAuth2 authorize，获取code
    resp = session.get(full_url, allow_redirects=False, timeout=10)

    if resp.status_code == 302:
        location = resp.headers.get('Location', '')
        # 从location中提取code
        code_match = re.search(r'code=([a-f0-9]+)', location)
        if code_match:
            oauth_code = code_match.group(1)
            print(f"[OAuth2] 获取到code: {oauth_code}")

            # 第二步：用code访问回调URL，获取access_token cookie
            callback_url = location
            resp2 = session.get(callback_url, allow_redirects=False, timeout=10)

            # 从Set-Cookie中获取access_token
            access_token = None
            refresh_token = None
            for cookie_name, cookie_value in session.cookies.items():
                if cookie_name == 'access_token':
                    access_token = cookie_value
                elif cookie_name == 'refresh_token':
                    refresh_token = cookie_value

            # 也检查Set-Cookie头
            if not access_token and 'Set-Cookie' in resp2.headers:
                set_cookie = resp2.headers['Set-Cookie']
                token_match = re.search(r'access_token=([a-f0-9]+)', set_cookie)
                if token_match:
                    access_token = token_match.group(1)
                refresh_match = re.search(r'refresh_token=([a-f0-9]+)', set_cookie)
                if refresh_match:
                    refresh_token = refresh_match.group(1)

            return access_token, refresh_token

    return None, None

# ==================== 二维码展示 ====================

def show_qr(qr_url):
    """在终端中展示二维码（方块字符），macOS 下同时生成图片并弹出"""
    if sys.platform == "darwin":
        # macOS: 生成图片并自动打开
        img = qrcode.QRCode(version=3, border=2, error_correction=qrcode.constants.ERROR_CORRECT_H)
        img.add_data(qr_url)
        img.make(fit=True)
        img_path = "/tmp/oa_qrcode.png"
        img.make_image(fill_color="black", back_color="white").save(img_path)
        subprocess.run(["open", img_path])
        print(f"\n✅ 二维码图片已弹出（macOS 图片查看器）")
        print(f"   如未看到，请手动打开: open {img_path}\n")
    else:
        # Windows/Linux: 终端 ASCII 二维码
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        os.system('mode con: cols=120 >nul 2>&1')
        qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(qr_url)
        qr.make(fit=True)
        print("\n请用 OA App 扫描下方二维码登录：\n")
        qr.print_ascii(invert=True)
        print()

def close_qr():
    """终端二维码无需关闭，保留空函数兼容调用"""
    pass

# ==================== 主流程 ====================
def main():
    # 如果本地已存有 access_token，直接读取返回
    if os.path.exists(TOKEN_FILE):
        print("\n" + "=" * 60)
        print(f"  检测到本地已存有 {TOKEN_FILE}，直接读取：")
        with open(TOKEN_FILE, "r") as f:
            print(f.read().strip())
        print("=" * 60)
        return

    session = new_session()

    # Step 1: 生成二维码
    qrcodeid = create_qr(session)
    qr_url = f"{QR_LOGIN_URL}?code={qrcodeid}"

    show_qr(qr_url)

    # 获取state
    state = None

    # Step 2: 轮询等待扫码和确认
    create_time = time.time()
    token = None

    while True:
        # 过期刷新
        if time.time() - create_time > 60:
            print("\n[过期] 刷新二维码...")
            qrcodeid = create_qr(session)
            qr_url = f"{QR_LOGIN_URL}?code={qrcodeid}"
            show_qr(qr_url)
            create_time = time.time()

        try:
            result = poll_scan(session, qrcodeid)
        except Exception:
            print("x", end="", flush=True)
            time.sleep(0.5)
            continue

        if result.get('invalid'):
            print("\n[失效] 二维码已失效，刷新...")
            qrcodeid = create_qr(session)
            qr_url = f"{QR_LOGIN_URL}?code={qrcodeid}"
            show_qr(qr_url)
            create_time = time.time()
            continue

        if result.get('scanned'):
            print(f"\n[扫码] 已扫描！等待确认...")
            close_qr()
            # 继续轮询等待token
            while True:
                time.sleep(0.5)
                login_result = do_login(session, qrcodeid)
                if login_result.get('token'):
                    token = login_result['token']
                    print(f"[确认] 获取token: {token}")
                    break
                print(",", end="", flush=True)
            break
        else:
            print(".", end="", flush=True)
            time.sleep(0.5)

    if not token:
        print("[错误] 未获取到token")
        return

    # Step 4: OAuth2登录
    print("\n[Step 4] OAuth2授权...")
    redirect_url = oauth2_login(session, token, state)

    if redirect_url and redirect_url != "success":
        print(f"  authorize URL: {redirect_url}")
        # Step 5: 通过重定向获取access_token
        print("\n[Step 5] 获取access_token...")
        access_token, refresh_token = get_access_token(session, redirect_url, state)
    else:
        # login直接返回success，尝试直接获取access_token
        print("  login返回success，直接检查cookies")
        access_token = session.cookies.get('access_token')
        refresh_token = session.cookies.get('refresh_token')

        if not access_token:
            # 尝试访问OAuth2 authorize获取code
            print("\n[Step 5] 尝试OAuth2 authorize...")
            oauth_url = f"{SSO_BASE}/rest/oauth2/authorize"
            params = {
                'response_type': 'code',
                'redirect_uri': REDIRECT_URI,
                'state': state or 'script-login',
                'client_id': CLIENT_ID,
            }
            resp = session.get(oauth_url, params=params, allow_redirects=False, timeout=10)
            print(f"  status: {resp.status_code}")

            if resp.status_code == 302:
                location = resp.headers.get('Location', '')
                print(f"  redirect: {location}")
                # 访问回调获取access_token
                resp2 = session.get(location, allow_redirects=False, timeout=10)
                access_token = session.cookies.get('access_token')
                refresh_token = session.cookies.get('refresh_token')

                # 也从Set-Cookie头中查找
                if not access_token and 'Set-Cookie' in resp2.headers:
                    token_match = re.search(r'access_token=([a-f0-9]+)', resp2.headers['Set-Cookie'])
                    if token_match:
                        access_token = token_match.group(1)

    print("\n" + "=" * 60)
    if access_token:
        print(f"  access_token:  {access_token}")
        print(f"  refresh_token: {refresh_token or 'N/A'}")
        print("=" * 60)

        # 保存到文件
        with open(TOKEN_FILE, "w") as f:
            f.write(f"access_token={access_token}\n")
            if refresh_token:
                f.write(f"refresh_token={refresh_token}\n")
        print(f"\n  已保存到: {TOKEN_FILE}")
    else:
        print("[失败] 未获取到access_token")
        print("所有cookies:", dict(session.cookies))
    print("=" * 60)

if __name__ == "__main__":
    main()
