# -*- utf-8 -*-
"""
使用 Python 调用腾讯文档 API 创建文档
"""
import subprocess
import json
import sys

def create_doc(title, content):
    """创建腾讯文档"""
    args = {
        'title': title,
        'content': content
    }
    
    result = subprocess.run(
        ['mcporter', 'call', 'tencent-docs', 'create_smartcanvas_by_mdx', '--args', json.dumps(args, ensure_ascii=False)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print("返回码:", result.returncode)
    print("STDOUT:", result.stdout[:500])
    print("STDERR:", result.stderr[:500])
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout.strip())
            print("\n解析成功!")
            print("响应:", json.dumps(response, indent=2, ensure_ascii=False))
            
            if 'error' in response and (not response['error'] or response['error'] == ''):
                file_id = response.get('file_id', response.get('node_id', ''))
                url = response.get('url', f'https://docs.qq.com/doc/{file_id}')
                return url, file_id
            else:
                print(f"错误：{response.get('error', '未知错误')}")
        except Exception as e:
            print(f"解析失败：{e}")
    
    return None, None

if __name__ == '__main__':
    title = "OA 邮件分析测试"
    content = "# 测试\n\n这是测试内容"
    
    url, file_id = create_doc(title, content)
    
    if url:
        print(f"\n✅ 创建成功!")
        print(f"   URL: {url}")
        print(f"   File ID: {file_id}")
    else:
        print("\n❌ 创建失败")
