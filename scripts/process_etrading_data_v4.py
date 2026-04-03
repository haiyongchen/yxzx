# -*- coding: utf-8 -*-
"""
处理e交易数据整合 - 根据图片要求添加多列收益统计
"""

import pandas as pd
import os
from pathlib import Path
import numpy as np
import re

def parse_percentage(val):
    """解析百分比字符串为数值"""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    # 提取数字部分
    match = re.search(r'[-+]?[\d,]+\.?\d*', val_str)
    if match:
        num_str = match.group().replace(',', '')
        try:
            return float(num_str)
        except:
            return np.nan
    return np.nan

def process_etrading_data():
    # 设置显示选项
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    # 文件路径
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    stats_file = base_dir / "专区接入情况统计表.xlsx"
    revenue_dir = base_dir / "e交易收益情况"
    
    print("=" * 60)
    print("开始处理e交易数据整合")
    print("=" * 60)
    
    # 读取专区接入情况统计表
    print(f"\n1. 读取统计表: {stats_file}")
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    print(f"   统计表行数: {len(df_stats)}")
    print(f"   统计表列数: {len(df_stats.columns)}")
    
    # 获取收益文件列表
    revenue_files = [f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")]
    print(f"\n2. 找到 {len(revenue_files)} 个收益文件")
    
    # 根据文件名识别不同类型的收益文件
    file_mapping = {}
    for f in revenue_files:
        fname = f.name
        if "25年" in fname or "2025" in fname:
            file_mapping['2025'] = f
        elif "26年3月" in fname or "2026年3月" in fname:
            if "总收益" in fname or "截至" in fname:
                file_mapping['2026_total'] = f
            else:
                file_mapping['2026_month'] = f
        elif "26年" in fname or "2026" in fname:
            file_mapping['2026_total'] = f
    
    print("   文件分类:")
    for key, f in file_mapping.items():
        print(f"     {key}: {f.name}")
    
    # 读取各类收益数据
    revenue_data = {}
    
    for key, file_path in file_mapping.items():
        print(f"\n3. 读取 {key} 数据: {file_path.name}")
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            revenue_data[key] = df
            print(f"   行数: {len(df)}")
        except Exception as e:
            print(f"   读取失败: {e}")
    
    # 找到统计表中的平台名称列
    stats_platform_col = None
    for i, col in enumerate(df_stats.columns):
        col_str = str(col)
        if '平台' in col_str:
            stats_platform_col = col
            print(f"\n4. 找到统计表平台列: {col} (索引{i})")
            break
    
    if stats_platform_col is None:
        stats_platform_col = df_stats.columns[8]
        print(f"\n4. 使用默认平台列: {stats_platform_col}")
    
    # 初始化新列
    df_stats['e交易26年3月_实得收益'] = 0.0
    df_stats['e交易26年3月_收益同比'] = np.nan
    df_stats['e交易26年3月_收益环比'] = np.nan
    df_stats['e交易26年总收益_截至3月25日'] = 0.0
    df_stats['e交易25年总收益'] = 0.0
    df_stats['e交易总收益_截至2026年3月25日'] = 0.0
    df_stats['e交易总项目数'] = 0
    
    # 处理2026年3月数据（当月）
    if '2026_month' in revenue_data:
        df_month = revenue_data['2026_month']
        cols = list(df_month.columns)
        platform_col = cols[3]  # 平台名称
        revenue_col = cols[8]   # 实得收益
        yoy_col = cols[10]      # 收益同比
        mom_col = cols[9]       # 收益环比
        
        # 按平台名称分组，求和收益
        month_revenue = df_month.groupby(platform_col)[revenue_col].sum()
        
        # 对于同比和环比，取第一个非空值（因为同一平台的同比环比应该相同）
        month_yoy = df_month.groupby(platform_col)[yoy_col].first()
        month_mom = df_month.groupby(platform_col)[mom_col].first()
        
        # 匹配并填充
        for platform in month_revenue.index:
            mask = df_stats[stats_platform_col] == platform
            if mask.any():
                df_stats.loc[mask, 'e交易26年3月_实得收益'] = month_revenue[platform]
                if platform in month_yoy.index:
                    df_stats.loc[mask, 'e交易26年3月_收益同比'] = parse_percentage(month_yoy[platform])
                if platform in month_mom.index:
                    df_stats.loc[mask, 'e交易26年3月_收益环比'] = parse_percentage(month_mom[platform])
    
    # 处理2026年总收益数据
    if '2026_total' in revenue_data:
        df_total = revenue_data['2026_total']
        cols = list(df_total.columns)
        platform_col = cols[3]   # 平台名称
        revenue_col = cols[8]    # 实得收益
        project_col = cols[5]    # 项目数
        
        total_summary = df_total.groupby(platform_col).agg({
            revenue_col: 'sum',
            project_col: 'sum'
        })
        
        for platform in total_summary.index:
            mask = df_stats[stats_platform_col] == platform
            if mask.any():
                df_stats.loc[mask, 'e交易26年总收益_截至3月25日'] = total_summary.loc[platform, revenue_col]
                df_stats.loc[mask, 'e交易总项目数'] = int(total_summary.loc[platform, project_col])
    
    # 处理2025年总收益数据
    if '2025' in revenue_data:
        df_2025 = revenue_data['2025']
        cols = list(df_2025.columns)
        platform_col = cols[3]   # 平台名称
        revenue_col = cols[8]    # 实得收益
        
        summary_2025 = df_2025.groupby(platform_col)[revenue_col].sum()
        
        for platform in summary_2025.index:
            mask = df_stats[stats_platform_col] == platform
            if mask.any():
                df_stats.loc[mask, 'e交易25年总收益'] = summary_2025[platform]
    
    # 计算总收益（25年 + 26年）
    df_stats['e交易总收益_截至2026年3月25日'] = (
        df_stats['e交易25年总收益'] + df_stats['e交易26年总收益_截至3月25日']
    )
    
    # 统计匹配情况
    print("\n5. 匹配统计:")
    matched_26_month = (df_stats['e交易26年3月_实得收益'] > 0).sum()
    matched_26_total = (df_stats['e交易26年总收益_截至3月25日'] > 0).sum()
    matched_25 = (df_stats['e交易25年总收益'] > 0).sum()
    matched_total = (df_stats['e交易总收益_截至2026年3月25日'] > 0).sum()
    
    print(f"   26年3月有收益的平台数: {matched_26_month}")
    print(f"   26年总收益有数据的平台数: {matched_26_total}")
    print(f"   25年有收益的平台数: {matched_25}")
    print(f"   总收益有数据的平台数: {matched_total}")
    
    # 保存结果
    output_file = base_dir / "专区接入情况统计表_已整合.xlsx"
    df_stats.to_excel(output_file, index=False)
    print(f"\n6. 已保存到: {output_file}")
    
    # 显示部分结果
    print("\n7. 处理结果预览（前5行有收益数据）:")
    preview_cols = [
        stats_platform_col,
        'e交易26年3月_实得收益',
        'e交易26年3月_收益同比',
        'e交易26年3月_收益环比',
        'e交易26年总收益_截至3月25日',
        'e交易25年总收益',
        'e交易总收益_截至2026年3月25日',
        'e交易总项目数'
    ]
    
    # 显示有收益数据的行
    has_revenue = df_stats[df_stats['e交易总收益_截至2026年3月25日'] > 0]
    if len(has_revenue) > 0:
        print(has_revenue[preview_cols].head())
    else:
        print("   暂无有收益数据的平台")
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    process_etrading_data()
