#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将zones_output.xlsx的专区地址填充到专区接入情况统计表的R列
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


def main():
    logger.info("=" * 60)
    logger.info("开始填充专区地址到R列")
    logger.info("=" * 60)
    
    # 1. 读取zones_output.xlsx（抓取到的329个专区）
    logger.info("读取 zones_output.xlsx...")
    zones_df = pd.read_excel('zones_output.xlsx')
    logger.info(f"读取到 {len(zones_df)} 个专区URL")
    
    # 2. 读取专区接入情况统计表
    stats_file = r'C:\Users\63111\.openclaw\media\inbound\专区接入情况统计表---f7021fc9-82d3-426b-8386-ea052c64a3d5.xlsx'
    logger.info(f"读取 专区接入情况统计表...")
    stats_df = pd.read_excel(stats_file)
    logger.info(f"读取到 {len(stats_df)} 条记录")
    
    # 清理列名
    stats_df.columns = [col.strip() for col in stats_df.columns]
    
    # 确认R列是"专区地址"
    if '专区地址' not in stats_df.columns:
        logger.error("统计表中没有'专区地址'列")
        return
    
    # 3. 创建匹配字典（专区名称 -> URL）
    url_dict = {}
    for _, row in zones_df.iterrows():
        name = str(row['专区名称']).strip()
        url = str(row['专区地址']).strip()
        if name and url:
            url_dict[name] = url
            # 同时存储简化版本
            simple_name = re.sub(r'(专区|平台|电子交易|招标采购|招采|交易|采购)$', '', name)
            if simple_name and simple_name != name:
                url_dict[simple_name] = url
    
    logger.info(f"创建了 {len(url_dict)} 个名称映射")
    
    # 4. 匹配并填充
    matched_count = 0
    similarity_matches = 0
    
    for idx in range(len(stats_df)):
        # 如果已有地址，跳过
        current_url = stats_df.at[idx, '专区地址']
        if pd.notna(current_url) and str(current_url).strip():
            continue
        
        # 获取专区名称
        zone_name = stats_df.at[idx, '专区名称']
        if pd.isna(zone_name):
            continue
        
        zone_name = str(zone_name).strip()
        
        # 尝试直接匹配
        matched = False
        if zone_name in url_dict:
            stats_df.at[idx, '专区地址'] = url_dict[zone_name]
            matched_count += 1
            matched = True
            logger.info(f"[精确匹配] {zone_name}")
        else:
            # 尝试简化名称匹配
            simple_name = re.sub(r'(专区|平台|电子交易|招标采购|招采|交易|采购)$', '', zone_name)
            if simple_name in url_dict:
                stats_df.at[idx, '专区地址'] = url_dict[simple_name]
                matched_count += 1
                matched = True
                logger.info(f"[简化匹配] {zone_name}")
            else:
                # 尝试模糊匹配（相似度>0.85）
                best_match = None
                best_score = 0
                for name_in_dict, url in url_dict.items():
                    score = similar(zone_name, name_in_dict)
                    if score > best_score and score > 0.85:
                        best_score = score
                        best_match = url
                
                if best_match:
                    stats_df.at[idx, '专区地址'] = best_match
                    similarity_matches += 1
                    matched = True
                    logger.info(f"[模糊匹配 {best_score:.2f}] {zone_name}")
        
        if matched and matched_count % 50 == 0:
            logger.info(f"进度: 已匹配 {matched_count} 条")
    
    # 5. 统计结果
    total_with_url = stats_df['专区地址'].notna().sum()
    missing = stats_df['专区地址'].isna().sum()
    fill_rate = total_with_url / len(stats_df) * 100
    
    logger.info("=" * 60)
    logger.info("填充完成!")
    logger.info(f"精确匹配: {matched_count} 条")
    logger.info(f"模糊匹配: {similarity_matches} 条")
    logger.info(f"总计填充: {matched_count + similarity_matches} 条")
    logger.info(f"当前已有地址: {total_with_url} 条")
    logger.info(f"仍缺失: {missing} 条")
    logger.info(f"填充率: {fill_rate:.1f}%")
    logger.info("=" * 60)
    
    # 6. 保存结果（覆盖原文件或创建新文件）
    output_path = '专区接入情况统计表_R列已填充.xlsx'
    stats_df.to_excel(output_path, index=False, engine='openpyxl')
    logger.info(f"结果已保存到: {output_path}")
    
    # 7. 显示前20条有地址的记录
    print("\n前20条已填充的记录:")
    filled = stats_df[stats_df['专区地址'].notna()].head(20)
    print(filled[['专区名称', '专区地址']].to_string())
    
    print("\n✓ 执行完成!")


if __name__ == '__main__':
    main()
