#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新抓取所有专区并进行智能匹配填充
"""

import pandas as pd
import time
import re
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def similar(a, b):
    """计算相似度"""
    if pd.isna(a) or pd.isna(b):
        return 0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


def fetch_all_zones():
    """重新抓取所有专区"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        logger.info("打开页面...")
        driver.get("https://www.etrading.cn/")
        time.sleep(3)
        
        # 获取页面源码
        page_source = driver.page_source
        
        # 使用正则匹配所有专区链接
        # 匹配: <a href="http://xxx.etrading.cn/" target="_blank">专区名称</a>
        pattern = r'<a\s+href="(https?://[^"]*etrading\.cn[^"]*)"[^>]*target="_blank"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, page_source)
        
        zones = {}
        for url, name in matches:
            name = name.strip()
            if name and url.startswith('http') and 'etrading.cn' in url:
                zones[name] = url
        
        driver.quit()
        logger.info(f"抓取到 {len(zones)} 个专区")
        return zones
        
    except Exception as e:
        logger.error(f"抓取失败: {e}")
        return {}


def smart_match(zone_name, zones_dict):
    """智能匹配"""
    if pd.isna(zone_name):
        return None
    
    zone_name = str(zone_name).strip()
    
    # 1. 直接匹配
    if zone_name in zones_dict:
        return zones_dict[zone_name]
    
    # 2. 去除后缀匹配
    suffixes = ['专区', '平台', '电子交易', '招标采购', '招采', '交易', '采购', '服务']
    for suffix in suffixes:
        simple_name = zone_name.replace(suffix, '')
        if simple_name in zones_dict:
            return zones_dict[simple_name]
    
    # 3. 模糊匹配（相似度>0.7）
    best_match = None
    best_score = 0
    for name, url in zones_dict.items():
        score = similar(zone_name, name)
        if score > best_score and score > 0.7:
            best_score = score
            best_match = url
    
    return best_match


def main():
    # 1. 读取当前表
    logger.info("读取专区接入情况统计表_R列已填充.xlsx...")
    df = pd.read_excel('专区接入情况统计表_R列已填充.xlsx')
    
    missing_before = df['专区地址'].isna().sum()
    logger.info(f"当前缺失地址: {missing_before} 条")
    
    # 2. 重新抓取所有专区
    logger.info("\n重新抓取所有专区...")
    zones = fetch_all_zones()
    
    if not zones:
        logger.error("抓取失败")
        return
    
    # 3. 智能匹配填充
    logger.info("\n智能匹配填充...")
    filled = 0
    
    for idx in range(len(df)):
        if pd.notna(df.at[idx, '专区地址']):
            continue
        
        zone_name = df.at[idx, '专区名称']
        url = smart_match(zone_name, zones)
        
        if url:
            df.at[idx, '专区地址'] = url
            filled += 1
            if filled % 10 == 0:
                logger.info(f"已填充 {filled} 条")
    
    # 4. 保存结果
    output_path = '专区接入情况统计表_完整填充.xlsx'
    df.to_excel(output_path, index=False)
    
    # 5. 统计
    missing_after = df['专区地址'].isna().sum()
    logger.info("\n" + "="*60)
    logger.info("填充完成!")
    logger.info(f"本次填充: {filled} 条")
    logger.info(f"填充前缺失: {missing_before} 条")
    logger.info(f"填充后缺失: {missing_after} 条")
    logger.info(f"总填充率: {df['专区地址'].notna().sum()/len(df)*100:.1f}%")
    logger.info(f"输出文件: {output_path}")
    logger.info("="*60)


if __name__ == '__main__':
    main()
