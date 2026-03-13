# -*- coding: utf-8 -*-
"""
使用已打开的 Chrome 访问小红书搜索
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from pathlib import Path

def search_xiaohongshu_chrome():
    """通过 Chrome 搜索小红书"""
    
    output_dir = Path("D:/openclaw-workspace/output")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("通过 Chrome 访问小红书搜索")
    print("=" * 60)
    
    chrome_options = Options()
    chrome_options.debugger_address = "localhost:9222"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # 搜索 URL
        search_url = "https://www.xiaohongshu.com/search_result?keyword=openclaw&source=web_search_result_notes"
        
        print(f"\n导航到：{search_url}")
        driver.get(search_url)
        
        # 等待加载
        print("等待页面加载...")
        for i in range(20, 0, -1):
            time.sleep(1)
            if i % 5 == 0:
                print(f"  {i}秒...")
        
        # 获取页面标题
        print(f"\n页面标题：{driver.title}")
        
        # 获取页面文本
        print("获取页面内容...")
        body_text = driver.find_element('tag name', 'body').text
        
        print(f"文本长度：{len(body_text)}")
        
        # 保存文本
        text_file = output_dir / "xiaohongshu_text.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(body_text)
        print(f"✅ 文本已保存：{text_file}")
        
        # 查找笔记相关内容
        print("\n查找笔记内容...")
        lines = body_text.split('\n')
        
        # 过滤包含关键词的行
        keywords = ['openclaw', 'OpenClaw', '笔记', '点赞', '收藏', '评论']
        matched_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 200:
                if any(kw in line for kw in keywords):
                    matched_lines.append(line)
        
        print(f"匹配的行：{len(matched_lines)}")
        
        # 去重
        unique_lines = list(dict.fromkeys(matched_lines))
        print(f"去重后：{len(unique_lines)}")
        
        # 保存匹配的内容
        if unique_lines:
            matched_file = output_dir / "xiaohongshu_matched.txt"
            with open(matched_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(unique_lines[:50]))
            print(f"✅ 匹配内容已保存：{matched_file}")
            
            # 打印预览
            print("\n内容预览 (Top 5):")
            for i, line in enumerate(unique_lines[:5]):
                print(f"\n{i+1}. {line[:150]}")
        
        # 截图
        screenshot = output_dir / "xiaohongshu_screenshot.png"
        driver.save_screenshot(str(screenshot))
        print(f"\n截图已保存：{screenshot}")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_xiaohongshu_chrome()
