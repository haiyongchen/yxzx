#!/usr/bin/env python3
import requests
import json
import os
import sys

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TOKEN_FILE = os.path.join(BASE_DIR, "access_token.txt")

OA_BASE = "https://oa.epoint.com.cn/oaextend/rest"

def get_token():
    """获取本地 Token"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            for line in f:
                if line.startswith("access_token="):
                    return line.split("=")[1].strip()
    return None

def fetch_data(url, data_dict):
    """通用的请求封装"""
    token = get_token()
    if not token:
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    
    try:
        resp = requests.post(url, headers=headers, data=data_dict, timeout=20, verify=False)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            print("[Error] Token 已过期，请先重新登录", file=sys.stderr)
            return None
    except Exception as e:
        print(f"[Error] 请求异常: {e}", file=sys.stderr)
    return None

def render_params_table(params_json, title="参数列表"):
    """解析并渲染层级化的参数表格"""
    if not params_json:
        return ""
    try:
        params_list = json.loads(params_json)
        if not params_list:
            return ""
        
        # 构建层级关系
        param_dict = {p.get('UID'): p for p in params_list}
        children_map = {}
        roots = []
        for p in params_list:
            parent_uid = p.get('ParentTaskUID')
            # 常见父节点标识为 -1, None 或空字符串，或者不在字典中的 UID
            if parent_uid in (-1, "-1", None, "") or parent_uid not in param_dict:
                roots.append(p)
            else:
                if parent_uid not in children_map:
                    children_map[parent_uid] = []
                children_map[parent_uid].append(p)

        output = f"\n#### {title}\n\n"
        output += "| 参数名 | 类型 | 必填 | 描述 |\n"
        output += "| :--- | :--- | :--- | :--- |\n"
        
        def walk(p, level=0):
            nonlocal output
            # 使用 HTML 空格实现 Markdown 表格内的缩进
            indent = "&nbsp;" * (level * 4) if level > 0 else ""
            req_str = "是" if p.get("required") else "否"
            name = p.get('name') or 'N/A'
            desc = p.get('desc') or p.get('description') or ""
            # 去除描述中的换行以防破坏表格布局
            desc = desc.replace("\n", " ").replace("\r", "")
            
            output += f"| {indent}`{name}` | {p.get('type') or ''} | {req_str} | {desc} |\n"
            
            uid = p.get('UID')
            if uid and uid in children_map:
                # 按 ordernumber 或名称排序（如果有的话）
                for child in children_map[uid]:
                    walk(child, level + 1)

        for root in roots:
            walk(root)
        
        return output
    except Exception as e:
        return f"\n> [Error] 解析{title}失败: {e}\n"

def main():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
    
    sys.stdout.reconfigure(encoding='utf-8')
    
    print(">>> 正在启动 OA 接口清单更新程序...")
    
    # ... 后续逻辑保持不变，但调用新的渲染函数 ...
    
    # 1. 获取根分类并找到 "nexbot接口资产"
    print("正在搜索 'nexbot接口资产' 根分类...")
    cat_url = f"{OA_BASE}/apiinnerservice/getApiShareCategory"
    root_cat_resp = fetch_data(cat_url, {"parentGuid": ""})
    
    if not root_cat_resp or not root_cat_resp.get("success"):
        print("[Critical] 无法获取根分类信息。")
        return

    target_guid = None
    for item in root_cat_resp.get("data", []):
        if item.get("shareClassName") == "nexbot接口资产":
            target_guid = item.get("rowguid")
            break
    
    if not target_guid:
        print("[Critical] 未能在根分类中找到 'nexbot接口资产'。")
        # 调试：打印出发现的根分类
        print("发现的根分类有:", [i.get('shareClassName') for i in root_cat_resp.get('data', [])])
        return

    print(f"找到目标分类 GUID: {target_guid}，正在获取子分类...")
    
    # 2. 获取目标分类下的子分类
    cats_resp = fetch_data(cat_url, {"parentGuid": target_guid})
    
    if not cats_resp or not cats_resp.get("success"):
        print(f"[Critical] 无法获取 {target_guid} 下的子分类。")
        return

    # 3. 遍历分类
    for cat in cats_resp["data"]:
        cat_name = cat["shareClassName"]
        cat_guid = cat["rowguid"]
        print(f"\n[分类] 正在处理: {cat_name} ({cat_guid})")
        
        # 获取该分类下的接口列表
        list_url = f"{OA_BASE}/apiinnerservice/getApiShareList"
        list_data = {"categoryGuid": cat_guid}
        api_list_resp = fetch_data(list_url, list_data)
        
        if not api_list_resp or not api_list_resp.get("success"):
            print(f"  [Error] 获取 {cat_name} 接口列表失败")
            continue
            
        md_content = f"# OA 接口清单 - {cat_name}\n\n"
        md_content += f"> 分类 GUID: `{cat_guid}`\n\n"
        
        # 3. 遍历并获取每个接口详情
        apis = api_list_resp["data"]
        print(f"  发现 {len(apis)} 个接口，正在拉取详情...")
        
        for api in apis:
            api_id = api["identification"]
            api_name = api["shareName"]
            print(f"    - {api_name} ({api_id})")
            
            detail_url = f"{OA_BASE}/apiinnerservice/findApiManageInfoById"
            detail_data = {"identification": api_id}
            detail_resp = fetch_data(detail_url, detail_data)
            
            # 兼容处理：有的接口直接返回对象，有的带 success/data 包装
            if detail_resp:
                info = detail_resp.get("data", detail_resp) if isinstance(detail_resp, dict) else {}
                
                # 如果没有获取到核心标识，说明可能真的失败了
                if not info.get("identification"):
                    md_content += f"## {api_name}\n- 详情获取失败 (`{api_id}`)\n\n---\n\n"
                    continue

                md_content += f"## {api_name}\n\n"
                md_content += f"| 属性 | 内容 |\n"
                md_content += f"| :--- | :--- |\n"
                md_content += f"| **标识符** | `{api_id}` |\n"
                md_content += f"| **API 路径** | `{info.get('apipath', 'N/A')}` |\n"
                md_content += f"| **请求方法** | `{info.get('method', 'POST')}` |\n"
                md_content += f"| **Content-Type** | `{info.get('requesttype', 'application/json')}` |\n"
                
                desc = info.get('description') or "无"
                md_content += f"| **描述** | {desc} |\n"
                
                # 请求参数 (层级化)
                md_content += render_params_table(info.get('requestparamsjson'), "请求参数")

                # 响应参数 (层级化)
                md_content += render_params_table(info.get('responseparamsjson'), "响应参数内容")

                # 示例代码
                req_ex = info.get('requestexample')
                if req_ex:
                    md_content += f"\n**请求示例:**\n```json\n{req_ex}\n```\n"
                
                res_ex = info.get('responseexample')
                if res_ex:
                    md_content += f"\n**响应示例:**\n```json\n{res_ex}\n```\n"

                # 如果有 SQL 或其它关键逻辑
                if info.get('mainsql'):
                    md_content += "\n**逻辑 (SQL/脚本):**\n"
                    md_content += f"```sql\n{info.get('mainsql')}\n```\n"
                
                md_content += "\n---\n\n"
            else:
                md_content += f"## {api_name}\n- 详情获取失败 (`{api_id}`)\n\n---\n\n"

        # 4. 写入 Markdown 文件
        # 移除非法字符
        safe_cat_name = "".join([c for c in cat_name if c.isalnum() or c in (' ', '-', '_')]).strip()
        file_path = os.path.join(ASSETS_DIR, f"{safe_cat_name}.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  [Done] 分类文件已生成: {file_path}")

    print("\n>>> 所有分类处理完毕！")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
