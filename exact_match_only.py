#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确匹配版本 - 只进行完全匹配，不匹配的不做操作
"""

import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_all_zones():
    """抓取所有专区"""
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


def main():
    # 1. 读取原始表（从未填充的版本开始）
    logger.info("读取原始表...")
    stats_file = r'C:\Users\63111\.openclaw\media\inbound\专区接入情况统计表---f7021fc9-82d3-426b-8386-ea052c64a3d5.xlsx'
    df = pd.read_excel(stats_file)
    df.columns = [col.strip() for col in df.columns]
    
    missing_before = df['专区地址'].isna().sum()
    logger.info(f"原始表缺失地址: {missing_before} 条")
    
    # 2. 抓取所有专区
    logger.info("\n抓取所有专区...")
    zones = fetch_all_zones()
    
    if not zones:
        logger.error("抓取失败")
        return
    
    # 3. 只进行精确匹配
    logger.info("\n进行精确匹配...")
    filled = 0
    
    for idx in range(len(df)):
        # 如果已有地址，跳过
        if pd.notna(df.at[idx, '专区地址']) and str(df.at[idx, '专区地址']).strip():
            continue
        
        zone_name = df.at[idx, '专区名称']
        if pd.isna(zone_name):
            continue
        
        zone_name = str(zone_name).strip()
        
        # 只进行完全匹配
        if zone_name in zones:
            df.at[idx, '专区地址'] = zones[zone_name]
            filled += 1
            logger.info(f"[精确匹配] {zone_name} -> {zones[zone_name]}")
    
    # 4. 保存结果
    output_path = '专区接入情况统计表_精确匹配.xlsx'
    df.to_excel(output_path, index=False)
    
    # 5. 统计
    missing_after = df['专区地址'].isna().sum()
    logger.info("\n" + "="*60)
    logger.info("精确匹配完成!")
    logger.info(f"总记录: {len(df)}")
    logger.info(f"匹配填充: {filled} 条")
    logger.info(f"填充前缺失: {missing_before} 条")
    logger.info(f"填充后缺失: {missing_after} 条")
    logger.info(f"填充率: {df['专区地址'].notna().sum()/len(df)*100:.1f}%")
    logger.info(f"输出文件: {output_path}")
    logger.info("="*60)
    
    # 显示未匹配的
    print("\n未匹配的专区 (前30条):")
    unmatched = df[df['专区地址'].isna()]['专区名称'].head(30).tolist()
    for i, name in enumerate(unmatched, 1):
        print(f"{i}. {name}")


if __name__ == '__main__':
    main()
