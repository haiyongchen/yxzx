---
name: epoint-oa-login
description: 新点 OA 系统自动登录工具。使用已保存的浏览器数据自动登录 OA 系统，支持登录状态过期后扫码更新。
metadata:
  {
    "openclaw": {
      "emoji": "🔐",
      "user-invocable": true,
      "requires": { "bins": ["python"], "python_packages": ["playwright"] }
    }
  }
---

# 新点 OA 系统自动登录 Skill

自动登录新点 OA 系统（oa.epoint.com.cn）及相关子系统（如 dui.epoint.com.cn）。

## 特性

- **自动登录**：使用已保存的浏览器用户数据自动登录
- **状态检测**：自动检测登录状态是否过期
- **扫码更新**：登录过期时自动提示用户扫码更新
- **多系统支持**：支持 OA 主站及各子系统（对账平台等）

## 配置

### 用户数据目录

登录状态保存在以下目录：
```
D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data
```

首次使用或登录过期时，需要扫码登录以更新此目录中的数据。

## 使用方法

### 打开 OA 首页

```python
from skills.epoint_oa_login import open_oa

# 自动登录 OA 系统
result = open_oa()
print(result)
# 输出: {'status': 'success', 'url': 'https://oa.epoint.com.cn/wboa9/', 'title': '...'}
```

### 打开指定 OA 子系统

```python
from skills.epoint_oa_login import open_oa_url

# 打开对账平台
result = open_oa_url('https://dui.epoint.com.cn/transferplatform/frame/fui/pages/themes/grace/grace?pageId=grace')
print(result)
```

### 检查登录状态

```python
from skills.epoint_oa_login import check_login_status

# 检查当前登录状态
status = check_login_status()
print(status)
# 输出: {'logged_in': True, 'url': '...', 'title': '...'} 或 {'logged_in': False}
```

### 更新登录状态（扫码登录）

```python
from skills.epoint_oa_login import refresh_login

# 强制刷新登录状态（会弹出浏览器让用户扫码）
result = refresh_login()
print(result)
```

## Python API

### `open_oa()`

自动登录 OA 系统并打开首页。

**返回：**
- `dict`: 包含 `status`, `url`, `title` 等信息
- 如果登录过期，会自动提示扫码更新

### `open_oa_url(url)`

使用已保存的登录状态打开指定的 OA 子系统 URL。

**参数：**
- `url` (str): 目标 URL

**返回：**
- `dict`: 包含 `status`, `url`, `title` 等信息

### `check_login_status()`

检查当前登录状态是否有效。

**返回：**
- `dict`: `{'logged_in': True/False, ...}`

### `refresh_login()`

强制刷新登录状态，弹出浏览器让用户扫码登录。

**返回：**
- `dict`: 包含 `status`, `message` 等信息

## 命令行使用

```bash
# 打开 OA 首页
python skills/epoint-oa-login/scripts/oa_login.py

# 打开指定 URL
python skills/epoint-oa-login/scripts/oa_login.py --url "https://dui.epoint.com.cn/transferplatform/..."

# 刷新登录状态（扫码登录）
python skills/epoint-oa-login/scripts/oa_login.py --refresh

# 检查登录状态
python skills/epoint-oa-login/scripts/oa_login.py --check
```

## 工作原理

1. **持久化浏览器数据**：使用 Playwright 的 `launch_persistent_context` 功能，将浏览器用户数据（Cookies、LocalStorage 等）保存到本地目录
2. **SSO 单点登录**：新点 OA 系统使用 SSO 机制，一次登录后可在多个子系统间共享登录状态
3. **自动检测**：通过检测页面 URL 和标题判断是否已登录
4. **过期处理**：检测到登录过期时，自动弹出浏览器让用户扫码更新

## 注意事项

1. **首次使用**：必须先执行 `refresh_login()` 或 `--refresh` 进行首次扫码登录
2. **登录有效期**：OA 系统的登录状态有一定有效期，过期后需要重新扫码
3. **浏览器选择**：默认使用 Chrome，如需使用 Edge 请修改配置
4. **数据安全**：用户数据目录包含敏感登录信息，请勿分享给他人
