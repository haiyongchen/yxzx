# -*- coding: utf-8 -*-
"""
处理e交易数据整合 - 正确的列对应关系
"""

import pandas as pd
from pathlib import Path
import numpy as np
import re

def parse_percentage(val):
    """解析百分比字符串为数值"""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    match = re.search(r'[-+]?[\d,]+\.?\d*', val_str)
    if match:
        num_str = match.group().replace(',', '')
        try:
            return float(num_str)
        except:
            return np.nan
    return np.nan

def process_etrading_data():
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    stats_file = base_dir / "专区接入情况统计表.xlsx"
    revenue_dir = base_dir / "e交易收益情况"
    
    print("=" * 60)
    print("开始处理e交易数据整合")
    print("=" * 60)
    
    # 读取统计表
    print(f"\n1. 读取统计表...")
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    print(f"   统计表行数: {len(df_stats)}")
    
    # 使用专区名称列（索引2，即C列）
    zone_col = df_stats.columns[2]  # 专区名称
    print(f"   专区名称列(C列): {zone_col}")
    
    # 获取收益文件
    revenue_files = [f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")]
    
    # 根据文件名识别不同类型的收益文件
    file_2025 = None
    file_2026_month = None
    file_2026_total = None
    file_total = None
    
    for f in revenue_files:
        fname = f.name
        # 根据文件名特征匹配
        if "25" in fname and "26" not in fname and "3月" not in fname:
            # 2025年总收益
            file_2025 = f
        elif "3月" in fname and "25日" not in fname:
            # 2026年3月收益
            file_2026_month = f
        elif "26" in fname and "截至" in fname:
            # 2026年截至3月25日
            file_2026_total = f
        elif "截至2026" in fname or "2026" in fname:
            # 总收益截至2026年3月25日
            file_total = f
    
    print(f"\n2. 找到收益文件:")
    print(f"   2025年总收益: {file_2025.name if file_2025 else '无'}")
    print(f"   2026年3月: {file_2026_month.name if file_2026_month else '无'}")
    print(f"   2026年截至3月25日: {file_2026_total.name if file_2026_total else '无'}")
    print(f"   总收益截至2026年3月25日: {file_total.name if file_total else '无'}")
    
    # 初始化新列（根据图片中的分类）
    print("\n3. 初始化新列...")
    
    # e交易26年3月收益情况
    df_stats['e交易26年3月_当月收益'] = 0.0
    df_stats['e交易26年3月_当月收益同比'] = np.nan
    df_stats['e交易26年3月_当月收益环比'] = np.nan
    
    # e交易26年收益情况（截至3月25日）
    df_stats['e交易26年_26年总收益'] = 0.0
    
    # e交易25年总收益情况
    df_stats['e交易25年_25年总收益'] = 0.0
    
    # e交易总收益情况（截至2026年3月25日）
    df_stats['e交易总收益_总收益'] = 0.0
    df_stats['e交易总收益_总项目数'] = 0
    
    # 处理2026年3月数据 -> 当月收益、当月收益同比、当月收益环比
    if file_2026_month:
        print("\n4. 处理2026年3月收益数据...")
        df_month = pd.read_excel(file_2026_month, sheet_name=0)
        
        platform_col = df_month.columns[3]   # D列：平台名称
        revenue_col = df_month.columns[8]    # 实得收益
        yoy_col = df_month.columns[10]       # 收益同比
        mom_col = df_month.columns[9]        # 收益环比
        
        print(f"   平台名称列(D列): {platform_col}")
        
        # 按平台名称分组汇总
        month_summary = df_month.groupby(platform_col).agg({
            revenue_col: 'sum',
            yoy_col: 'first',
            mom_col: 'first'
        })
        
        print(f"   收益数据平台数: {len(month_summary)}")
        
        # 匹配并填充数据
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in month_summary.index:
                df_stats.at[idx, 'e交易26年3月_当月收益'] = month_summary.loc[zone_name, revenue_col]
                df_stats.at[idx, 'e交易26年3月_当月收益同比'] = parse_percentage(month_summary.loc[zone_name, yoy_col])
                df_stats.at[idx, 'e交易26年3月_当月收益环比'] = parse_percentage(month_summary.loc[zone_name, mom_col])
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 处理2026年截至3月25日数据 -> 26年总收益
    if file_2026_total:
        print("\n5. 处理2026年收益数据（截至3月25日）...")
        df_2026 = pd.read_excel(file_2026_total, sheet_name=0)
        
        platform_col = df_2026.columns[3]   # D列：平台名称
        revenue_col = df_2026.columns[8]    # 实得收益
        
        summary_2026 = df_2026.groupby(platform_col)[revenue_col].sum()
        
        print(f"   收益数据平台数: {len(summary_2026)}")
        
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in summary_2026.index:
                df_stats.at[idx, 'e交易26年_26年总收益'] = summary_2026[zone_name]
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 处理2025年总收益数据 -> 25年总收益
    if file_2025:
        print("\n6. 处理2025年总收益数据...")
        df_2025 = pd.read_excel(file_2025, sheet_name=0)
        
        platform_col = df_2025.columns[3]   # D列：平台名称
        revenue_col = df_2025.columns[8]    # 实得收益
        
        summary_2025 = df_2025.groupby(platform_col)[revenue_col].sum()
        
        print(f"   收益数据平台数: {len(summary_2025)}")
        
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in summary_2025.index:
                df_stats.at[idx, 'e交易25年_25年总收益'] = summary_2025[zone_name]
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 处理总收益数据（截至2026年3月25日）-> 总收益、总项目数
    if file_total:
        print("\n7. 处理总收益数据（截至2026年3月25日）...")
        df_total = pd.read_excel(file_total, sheet_name=0)
        
        platform_col = df_total.columns[3]   # D列：平台名称
        revenue_col = df_total.columns[8]    # 实得收益
        project_col = df_total.columns[5]    # 项目数
        
        # 汇总收益和项目数
        total_summary = df_total.groupby(platform_col).agg({
            revenue_col: 'sum',
            project_col: 'sum'
        })
        
        print(f"   收益数据平台数: {len(total_summary)}")
        
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in total_summary.index:
                df_stats.at[idx, 'e交易总收益_总收益'] = total_summary.loc[zone_name, revenue_col]
                df_stats.at[idx, 'e交易总收益_总项目数'] = int(total_summary.loc[zone_name, project_col])
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 统计匹配情况
    print("\n8. 匹配统计:")
    matched_26_month = (df_stats['e交易26年3月_当月收益'] > 0).sum()
    matched_26_total = (df_stats['e交易26年_26年总收益'] > 0).sum()
    matched_25 = (df_stats['e交易25年_25年总收益'] > 0).sum()
    matched_total = (df_stats['e交易总收益_总收益'] > 0).sum()
    
    print(f"   26年3月有收益的平台数: {matched_26_month}")
    print(f"   26年总收益有数据的平台数: {matched_26_total}")
    print(f"   25年有收益的平台数: {matched_25}")
    print(f"   总收益有数据的平台数: {matched_total}")
    
    # 保存结果
    output_file = base_dir / "专区接入情况统计表_已整合_最终.xlsx"
    df_stats.to_excel(output_file, index=False)
    print(f"\n9. 已保存到: {output_file}")
    
    # 显示有收益的数据预览
    print("\n10. 有收益数据的平台预览（前10条）:")
    has_revenue = df_stats[df_stats['e交易总收益_总收益'] > 0]
    print(f"   共有 {len(has_revenue)} 个平台有收益数据")
    
    if len(has_revenue) > 0:
        preview_cols = [
            zone_col,
            'e交易26年3月_当月收益',
            'e交易26年3月_当月收益同比',
            'e交易26年3月_当月收益环比',
            'e交易26年_26年总收益',
            'e交易25年_25年总收益',
            'e交易总收益_总收益',
            'e交易总收益_总项目数'
        ]
        # 保存预览
        preview_file = base_dir / "收益数据预览_最终.txt"
        with open(preview_file, 'w', encoding='utf-8') as f:
            f.write("有收益数据的平台预览（前20条）:\n\n")
            f.write(has_revenue[preview_cols].head(20).to_string())
        print(f"   预览已保存到: {preview_file}")
        
        # 显示部分数据
        print("\n   数据示例:")
        print(has_revenue[preview_cols].head(5).to_string())
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

