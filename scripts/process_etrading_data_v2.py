# -*- coding: utf-8 -*-
"""
处理e交易数据整合
根据专区接入情况统计表和e交易收益情况文件，整合数据
"""

import pandas as pd
import os
from pathlib import Path
import numpy as np

def process_etrading_data():
    # 文件路径
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    stats_file = base_dir / "专区接入情况统计表.xlsx"
    revenue_dir = base_dir / "e交易收益情况"
    
    print(f"读取统计表: {stats_file}")
    
    # 读取专区接入情况统计表
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    
    # 显示列名
    print("\n统计表列名:")
    for i, col in enumerate(df_stats.columns):
        print(f"  {i}: {col}")
    
    # 获取收益文件夹中的所有Excel文件（排除临时文件）
    revenue_files = [f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")]
    print(f"\n找到 {len(revenue_files)} 个收益文件:")
    for f in revenue_files:
        print(f"  - {f.name}")
    
    # 读取所有收益数据并合并
    all_revenue_data = []
    for rev_file in revenue_files:
        print(f"\n读取: {rev_file.name}")
        try:
            df_rev = pd.read_excel(rev_file, sheet_name=0)
            # 添加数据来源标记
            df_rev['数据来源'] = rev_file.name
            all_revenue_data.append(df_rev)
        except Exception as e:
            print(f"  读取失败: {e}")
    
    if not all_revenue_data:
        print("\n没有读取到任何收益数据")
        return
    
    # 合并所有收益数据
    df_revenue = pd.concat(all_revenue_data, ignore_index=True)
    print(f"\n合并后收益数据总行数: {len(df_revenue)}")
    
    # 显示收益数据列名
    print("\n收益数据列名:")
    for i, col in enumerate(df_revenue.columns):
        print(f"  {i}: {col}")
    
    # 找到关键列
    # 假设平台名称列是第4列（索引3），实得收益列是第9列（索引8）
    # 根据实际输出调整
    platform_col = df_revenue.columns[3]  # 平台名称列
    revenue_col = df_revenue.columns[8]   # 实得收益列
    
    print(f"\n平台名称列: {platform_col}")
    print(f"实得收益列: {revenue_col}")
    
    # 按平台名称分组并求和实得收益
    revenue_summary = df_revenue.groupby(platform_col)[revenue_col].sum().reset_index()
    revenue_summary.columns = ['平台名称', '总收益']
    
    print(f"\n收益汇总（前10条）:")
    print(revenue_summary.head(10))
    
    # 找到统计表中用于匹配的平台名称列
    # 根据列名输出，可能是'交易平台'或类似的列
    stats_platform_col = None
    for col in df_stats.columns:
        if '平台' in str(col) or '交易' in str(col):
            stats_platform_col = col
            print(f"\n找到统计表平台列: {col}")
            break
    
    if stats_platform_col is None:
        # 如果没有找到，使用第9列（索引8）
        stats_platform_col = df_stats.columns[8]
        print(f"\n使用默认平台列: {stats_platform_col}")
    
    # 匹配并添加收益列
    # 根据图片中的分类，需要添加以下列：
    # 1. e交易26年3月收益情况 - 当月收益
    # 2. e交易26年3月收益情况 - 当月收益同比
    # 3. e交易26年3月收益情况 - 当月收益环比
    # 4. e交易26年收益情况（截至3月25日）- 26年总收益
    # 5. e交易25年总收益情况 - 25年总收益
    # 6. e交易总收益情况（截至2026年3月25日）- 总收益
    # 7. e交易总收益情况（截至2026年3月25日）- 总项目数
    
    # 简化处理：先添加总收益列
    df_stats['e交易总收益'] = df_stats[stats_platform_col].map(
        revenue_summary.set_index('平台名称')['总收益']
    )
    
    # 填充NaN为0
    df_stats['e交易总收益'] = df_stats['e交易总收益'].fillna(0)
    
    print(f"\n匹配完成，添加了 'e交易总收益' 列")
    print(f"有收益数据的平台数: {(df_stats['e交易总收益'] > 0).sum()}")
    
    # 保存处理后的数据
    output_file = base_dir / "专区接入情况统计表_已整合.xlsx"
    df_stats.to_excel(output_file, index=False)
    print(f"\n已保存到: {output_file}")
    
    # 显示部分结果
    print("\n处理结果预览（前5行）:")
    preview_cols = [stats_platform_col, 'e交易总收益']
    print(df_stats[preview_cols].head())

if __name__ == "__main__":
    process_etrading_data()
