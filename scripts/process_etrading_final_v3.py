# -*- coding: utf-8 -*-
"""
处理e交易数据整合 - 修复项目数格式问题
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

def parse_int(val):
    """解析为整数"""
    if pd.isna(val):
        return 0
    val_str = str(val).strip()
    # 提取数字部分
    match = re.search(r'\d+', val_str)
    if match:
        try:
            return int(match.group())
        except:
            return 0
    return 0

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
    
    # 使用专区名称列（索引2）
    zone_col = df_stats.columns[2]  # 专区名称
    print(f"   专区名称列: {zone_col}")
    
    # 获取收益文件
    revenue_files = [f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")]
    
    # 分类文件
    file_2025 = None
    file_2026_month = None
    file_2026_total = None
    
    for f in revenue_files:
        fname = f.name
        if "25年" in fname:
            file_2025 = f
        elif "26年3月" in fname and "总收益" not in fname:
            file_2026_month = f
        elif "26年" in fname or "2026" in fname:
            file_2026_total = f
    
    print(f"\n2. 找到收益文件:")
    print(f"   2025年: {file_2025.name if file_2025 else '无'}")
    print(f"   2026年3月: {file_2026_month.name if file_2026_month else '无'}")
    print(f"   2026年总: {file_2026_total.name if file_2026_total else '无'}")
    
    # 初始化新列
    print("\n3. 初始化新列...")
    df_stats['e交易26年3月_实得收益'] = 0.0
    df_stats['e交易26年3月_当月收益同比'] = np.nan
    df_stats['e交易26年3月_当月收益环比'] = np.nan
    df_stats['e交易26年总收益_截至3月25日'] = 0.0
    df_stats['e交易25年总收益'] = 0.0
    df_stats['e交易总收益_截至2026年3月25日'] = 0.0
    df_stats['e交易总项目数'] = 0
    
    # 处理2026年3月数据
    if file_2026_month:
        print("\n4. 处理2026年3月收益数据...")
        df_month = pd.read_excel(file_2026_month, sheet_name=0)
        
        platform_col = df_month.columns[3]   # 平台名称
        revenue_col = df_month.columns[8]    # 实得收益
        yoy_col = df_month.columns[10]       # 收益同比
        mom_col = df_month.columns[9]        # 收益环比
        
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
                df_stats.at[idx, 'e交易26年3月_实得收益'] = month_summary.loc[zone_name, revenue_col]
                df_stats.at[idx, 'e交易26年3月_当月收益同比'] = parse_percentage(month_summary.loc[zone_name, yoy_col])
                df_stats.at[idx, 'e交易26年3月_当月收益环比'] = parse_percentage(month_summary.loc[zone_name, mom_col])
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 处理2026年总收益数据
    if file_2026_total:
        print("\n5. 处理2026年总收益数据...")
        df_total = pd.read_excel(file_2026_total, sheet_name=0)
        
        platform_col = df_total.columns[3]   # 平台名称
        revenue_col = df_total.columns[8]    # 实得收益
        project_col = df_total.columns[5]    # 项目数
        
        # 只汇总收益，项目数单独处理
        total_revenue = df_total.groupby(platform_col)[revenue_col].sum()
        
        # 对于项目数，取第一个非空值
        total_projects = df_total.groupby(platform_col)[project_col].first()
        
        print(f"   收益数据平台数: {len(total_revenue)}")
        
        # 匹配并填充数据
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in total_revenue.index:
                df_stats.at[idx, 'e交易26年总收益_截至3月25日'] = total_revenue[zone_name]
                if zone_name in total_projects.index:
                    df_stats.at[idx, 'e交易总项目数'] = parse_int(total_projects[zone_name])
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 处理2025年收益数据
    if file_2025:
        print("\n6. 处理2025年收益数据...")
        df_2025 = pd.read_excel(file_2025, sheet_name=0)
        
        platform_col = df_2025.columns[3]   # 平台名称
        revenue_col = df_2025.columns[8]    # 实得收益
        
        summary_2025 = df_2025.groupby(platform_col)[revenue_col].sum()
        
        print(f"   收益数据平台数: {len(summary_2025)}")
        
        # 匹配并填充数据
        match_count = 0
        for idx, row in df_stats.iterrows():
            zone_name = str(row[zone_col]).strip()
            if zone_name in summary_2025.index:
                df_stats.at[idx, 'e交易25年总收益'] = summary_2025[zone_name]
                match_count += 1
        
        print(f"   匹配成功: {match_count} 条")
    
    # 计算总收益
    df_stats['e交易总收益_截至2026年3月25日'] = (
        df_stats['e交易25年总收益'] + df_stats['e交易26年总收益_截至3月25日']
    )
    
    # 统计匹配情况
    print("\n7. 匹配统计:")
    matched_26_month = (df_stats['e交易26年3月_实得收益'] > 0).sum()
    matched_26_total = (df_stats['e交易26年总收益_截至3月25日'] > 0).sum()
    matched_25 = (df_stats['e交易25年总收益'] > 0).sum()
    matched_total = (df_stats['e交易总收益_截至2026年3月25日'] > 0).sum()
    
    print(f"   26年3月有收益的平台数: {matched_26_month}")
    print(f"   26年总收益有数据的平台数: {matched_26_total}")
    print(f"   25年有收益的平台数: {matched_25}")
    print(f"   总收益有数据的平台数: {matched_total}")
    
    # 保存结果到新文件
    output_file = base_dir / "专区接入情况统计表_已整合.xlsx"
    
    # 如果文件已存在，先尝试删除
    if output_file.exists():
        try:
            output_file.unlink()
        except:
            pass
    
    df_stats.to_excel(output_file, index=False)
    print(f"\n8. 已保存到: {output_file}")
    
    # 显示有收益的数据预览
    print("\n9. 有收益数据的平台预览（前10条）:")
    has_revenue = df_stats[df_stats['e交易总收益_截至2026年3月25日'] > 0]
    print(f"   共有 {len(has_revenue)} 个平台有收益数据")
    
    if len(has_revenue) > 0:
        preview_cols = [
            zone_col,
            'e交易26年3月_实得收益',
            'e交易26年总收益_截至3月25日',
            'e交易25年总收益',
            'e交易总收益_截至2026年3月25日',
            'e交易总项目数'
        ]
        # 保存预览到文件
        preview_file = base_dir / "收益数据预览.txt"
        with open(preview_file, 'w', encoding='utf-8') as f:
            f.write("有收益数据的平台预览（前20条）:\n\n")
            f.write(has_revenue[preview_cols].head(20).to_string())
        print(f"   预览已保存到: {preview_file}")
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    process_etrading_data()
