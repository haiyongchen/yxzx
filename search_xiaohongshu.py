# -*- coding: utf-8 -*-
"""
直接访问小红书搜索 OpenClaw 相关内容
"""
import requests
import json
import re
from pathlib import Path

def search_xiaohongshu():
    """搜索小红书内容"""
    
    output_dir = Path("D:/openclaw-workspace/output")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("小红书搜索：OpenClaw")
    print("=" * 60)
    
    # 搜索 URL
    search_url = "https://www.xiaohongshu.com/search_result?keyword=openclaw&source=web_search_result_notes"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.xiaohongshu.com/',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print(f"\n访问：{search_url}")
        resp = session.get(search_url, timeout=30)
        print(f"状态码：{resp.status_code}")
        print(f"内容长度：{len(resp.text)}")
        
        # 保存 HTML
        html_file = output_dir / "xiaohongshu_search.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"✅ HTML 已保存：{html_file}")
        
        # 尝试提取笔记数据
        html = resp.text
        
        # 查找包含中文的 JSON 数据
        print("\n尝试提取笔记数据...")
        
        # 查找可能的笔记标题
        title_pattern = r'"title":"([^"]+)"'
        titles = re.findall(title_pattern, html)
        print(f"找到标题：{len(titles)} 个")
        
        # 查找用户信息
        user_pattern = r'"nickname":"([^"]+)"'
        users = re.findall(user_pattern, html)
        print(f"找到用户：{len(users)} 个")
        
        # 查找点赞数
        like_pattern = r'"likes":"([^"]+)"'
        likes = re.findall(like_pattern, html)
        print(f"找到点赞：{len(likes)} 个")
        
        # 保存提取的数据
        data = {
            "titles": titles[:20],
            "users": users[:20],
            "likes": likes[:20]
        }
        
        data_file = output_dir / "xiaohongshu_data.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已保存：{data_file}")
        
        # 打印预览
        print("\n找到的内容预览:")
        if titles:
            print("\n标题:")
            for i, t in enumerate(titles[:10]):
                print(f"  {i+1}. {t[:80]}")
        
        if users:
            print("\n用户:")
            for i, u in enumerate(users[:10]):
                print(f"  {i+1}. {u}")
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_xiaohongshu()
