# -*- utf-8 -*-
"""
独立腾讯文档创建脚本
"""
import subprocess
import json
import os
import sys
from datetime import datetime

# 设置 Token
os.environ['TENCENT_DOCS_TOKEN'] = 'e23255dcdf51491cb208ecc9cc341e21'

# 读取本地 Markdown 文件
md_file = 'D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md'
if not os.path.exists(md_file):
    print(f"❌ 文件不存在：{md_file}")
    sys.exit(1)

with open(md_file, 'r', encoding='utf-8') as f:
    content = f.read()

title = f"OA 邮件分析报表-{datetime.now().strftime('%Y%m%d')}"

print("=" * 60)
print("腾讯文档创建工具")
print("=" * 60)
print(f"\n📄 标题：{title}")
print(f"📝 内容长度：{len(content)} 字符")

# 创建临时 JSON 文件
import tempfile
params_file = os.path.join(tempfile.gettempdir(), 'tencent_doc_params.json')
params = {
    'title': title,
    'mdx': content
}
with open(params_file, 'w', encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False, indent=2)

print(f"\n💾 参数文件：{params_file}")

# 调用 mcporter（使用完整路径）
mcporter_path = 'D:/nvm4w/nodejs/mcporter.ps1'

print(f"\n🚀 调用 mcporter...")
print(f"   路径：{mcporter_path}")

try:
    result = subprocess.run(
        ['powershell', '-ExecutionPolicy', 'Bypass', '-File', mcporter_path, 
         'call', 'tencent-docs', 'create_smartcanvas_by_mdx', '--file', params_file],
        capture_output=True,
        text=True,
        timeout=30,
        env=os.environ
    )
    
    print(f"\n返回码：{result.returncode}")
    
    if result.stdout:
        print(f"输出：{result.stdout[:500]}")
    if result.stderr:
        print(f"错误：{result.stderr[:500]}")
    
    if result.returncode == 0:
        # 解析响应
        try:
            response = json.loads(result.stdout.strip())
            if 'error' in response and (not response['error'] or response['error'] == ''):
                file_id = response.get('file_id', response.get('node_id', ''))
                url = response.get('url', f'https://docs.qq.com/doc/{file_id}')
                print(f"\n✅ 创建成功！")
                print(f"   📄 文档 ID: {file_id}")
                print(f"   🔗 在线查看：{url}")
                sys.exit(0)
            else:
                print(f"\n❌ 创建失败：{response.get('error', '未知错误')}")
        except Exception as e:
            print(f"\n❌ 响应解析失败：{e}")
    else:
        print("\n❌ 调用失败")
        
except FileNotFoundError as e:
    print(f"\n❌ 找不到 mcporter: {e}")
    print("\n💡 请确认 mcporter 已安装:")
    print("   npm install -g mcporter")
except subprocess.TimeoutExpired:
    print("\n❌ 调用超时")
except Exception as e:
    print(f"\n❌ 错误：{e}")

sys.exit(1)
