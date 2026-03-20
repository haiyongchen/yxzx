#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专区地址匹配脚本
功能：将抓取到的329个专区URL与专区接入情况统计表进行匹配，填充缺失的专区地址
"""

import pandas as pd
import re
from difflib import SequenceMatcher
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def similar(a, b):
    """计算两个字符串的相似度"""
    if pd.isna(a) or pd.isna(b):
        return 0
    return SequenceMatcher(None, str(a), str(b)).ratio()


def match_zone_urls():
    """匹配专区地址"""
    
    # 读取两个Excel文件
    logger.info("读取文件...")
    
    # 1. 读取抓取到的329个专区URL
    zones_df = pd.read_excel('zones_output.xlsx')
    logger.info(f"读取到 {len(zones_df)} 个抓取到的专区URL")
    
    # 2. 读取专区接入情况统计表
    stats_file = r'C:\Users\63111\.openclaw\media\inbound\专区接入情况统计表---f7021fc9-82d3-426b-8386-ea052c64a3d5.xlsx'
    stats_df = pd.read_excel(stats_file)
    logger.info(f"读取到 {len(stats_df)} 条专区接入记录")
    
    # 清理列名（去除空格）
    stats_df.columns = [col.strip() for col in stats_df.columns]
    
    # 检查是否有专区地址列
    if '专区地址' not in stats_df.columns:
        logger.error("统计表中没有'专区地址'列")
        return False
    
    # 统计缺失地址的数量
    missing_before = stats_df['专区地址'].isna().sum()
    logger.info(f"匹配前缺失地址的记录: {missing_before} 条")
    
    # 创建匹配字典（专区名称 -> URL）
    url_dict = {}
    for _, row in zones_df.iterrows():
        name = str(row['专区名称']).strip()
        url = str(row['专区地址']).strip()
        if name and url:
            url_dict[name] = url
            # 同时存储简化版本（去除"专区"、"平台"等后缀）
            simple_name = re.sub(r'(专区|平台|电子交易|招标采购|招采|交易|采购)$', '', name)
            if simple_name:
                url_dict[simple_name] = url
    
    logger.info(f"创建了 {len(url_dict)} 个名称映射")
    
    # 匹配逻辑
    matched_count = 0
    similarity_matches = 0
    
    for idx in range(len(stats_df)):
        # 如果已有地址，跳过
        if pd.notna(stats_df.at[idx, '专区地址']) and str(stats_df.at[idx, '专区地址']).strip():
            continue
        
        # 获取专区名称
        zone_name = stats_df.at[idx, '专区名称']
        if pd.isna(zone_name):
            continue
        
        zone_name = str(zone_name).strip()
        
        # 尝试直接匹配
        if zone_name in url_dict:
            stats_df.at[idx, '专区地址'] = url_dict[zone_name]
            matched_count += 1
            logger.info(f"[精确匹配] {zone_name} -> {url_dict[zone_name]}")
            continue
        
        # 尝试简化名称匹配
        simple_name = re.sub(r'(专区|平台|电子交易|招标采购|招采|交易|采购)$', '', zone_name)
        if simple_name in url_dict:
            stats_df.at[idx, '专区地址'] = url_dict[simple_name]
            matched_count += 1
            logger.info(f"[简化匹配] {zone_name} -> {url_dict[simple_name]}")
            continue
        
        # 尝试模糊匹配（相似度>0.8）
        best_match = None
        best_score = 0
        
        for name_in_dict, url in url_dict.items():
            score = similar(zone_name, name_in_dict)
            if score > best_score and score > 0.8:
                best_score = score
                best_match = url
        
        if best_match:
            stats_df.at[idx, '专区地址'] = best_match
            similarity_matches += 1
            logger.info(f"[模糊匹配 {best_score:.2f}] {zone_name} -> {best_match}")
    
    # 统计结果
    missing_after = stats_df['专区地址'].isna().sum()
    filled_count = missing_before - missing_after
    
    logger.info("=" * 50)
    logger.info("匹配完成!")
    logger.info(f"精确匹配: {matched_count} 条")
    logger.info(f"模糊匹配: {similarity_matches} 条")
    logger.info(f"总计填充: {filled_count} 条")
    logger.info(f"仍缺失: {missing_after} 条")
    logger.info("=" * 50)
    
    # 保存结果
    output_path = '专区接入情况统计表_已填充.xlsx'
    stats_df.to_excel(output_path, index=False, engine='openpyxl')
    logger.info(f"结果已保存到: {output_path}")
    
    # 显示部分结果
    print("\n填充结果预览 (前20条有变化的):")
    changed = stats_df[stats_df['专区地址'].notna()].head(20)
    print(changed[['专区名称', '专区地址']].to_string())
    
    return True


if __name__ == '__main__':
    match_zone_urls()
