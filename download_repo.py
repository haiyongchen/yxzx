#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载GitHub仓库
"""

import requests
import zipfile
import os
import shutil

# 仓库信息
repo_url = "https://github.com/liscx/EPBiddingCount/archive/refs/heads/master.zip"
output_dir = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\专区统计代码"
zip_path = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\EPBiddingCount.zip"

print("开始下载...")

# 设置代理（如果需要）
proxies = {
    # 'http': 'http://127.0.0.1:7890',
    # 'https': 'http://127.0.0.1:7890',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    # 下载ZIP文件
    print(f"下载: {repo_url}")
    response = requests.get(repo_url, headers=headers, proxies=proxies, timeout=60)
    response.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    print(f"下载完成: {zip_path}")
    
    # 解压ZIP文件
    print("解压...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(output_dir))
    print("解压完成")
    
    # 重命名文件夹
    extracted_dir = os.path.join(os.path.dirname(output_dir), "EPBiddingCount-main")
    if os.path.exists(extracted_dir):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        shutil.move(extracted_dir, output_dir)
        print(f"重命名为: {output_dir}")
    
    # 删除ZIP文件
    os.remove(zip_path)
    print("清理完成")
    
    print("\n✓ 下载完成!")
    print(f"位置: {output_dir}")
    
    # 列出文件
    print("\n文件列表:")
    for item in os.listdir(output_dir):
        print(f"  - {item}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
