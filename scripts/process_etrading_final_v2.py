# -*- coding: utf-8 -*-
"""
处理e交易数据整合 - 最终版本
根据图片要求，在专区接入情况统计表中添加收益数据列
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
    
    print("=" * 60)
    print("开始处理e交易数据整合")
    print("=" * 60)
    
    # 读取专区接入情况统计表
    print(f"\n1. 读取统计表: {stats_file}")
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    print(f"   统计表行数: {len(df_stats)}")
    
    # 获取收益文件列表
    revenue_files = [f for f in revenue_dir.glob("*.xlsx") if not f.name.startswith("~$")]
    print(f"\n2. 找到 {len(revenue_files)} 个收益文件")
    
    # 分类收益文件
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
    
    print(f"   2025年收益文件: {file_2025.name if file_2025 else '无'}")
    print(f"   2026年3月收益文件: {file_2026_month.name if file_2026_month else '无'}")
    print(f"   2026年总收益文件: {file_2026_total.name if file_2026_total else '无'}")
    
    # 在统计表中添加新列（根据图片中的分类）
    print("\n3. 添加收益统计列...")
    
    # e交易26年3月收益情况
    df_stats['e交易26年3月_实得收益'] = 0.0
    df_stats['e交易26年3月_当月收益'] = 0.0
    df_stats['e交易26年3月_当月收益同比'] = np.nan
    df_stats['e交易26年3月_当月收益环比'] = np.nan
    
    # e交易26年收益情况（截至3月25日）
    df_stats['e交易26年_实得收益'] = 0.0
    df_stats['e交易26年_26年总收益'] = 0.0
    
    # e交易25年总收益情况
    df_stats['e交易25年_实得收益'] = 0.0
    df_stats['e交易25年_25年总收益'] = 0.0
    
    # e交易总收益情况（截至2026年3月25日）
    df_stats['e交易总收益_实得收益'] = 0.0
    df_stats['e交易总收益_总收益'] = 0.0
    df_stats['e交易总收益_项目数'] = 0
    df_stats['e交易总收益_总项目数'] = 0
    
    # 读取并处理2026年3月数据
    if file_2026_month:
        print("\n4. 处理2026年3月收益数据...")
        df_month = pd.read_excel(file_2026_month, sheet_name=0)
        
        # 按平台名称汇总
        platform_col = df_month.columns[3]  # 平台名称
        revenue_col = df_month.columns[8]   # 实得收益
        
        month_summary = df_month.groupby(platform_col)[revenue_col].sum()
        print(f"   3月收益平台数: {len(month_summary)}")
        print(f"   3月总收益: {month_summary.sum():.2f}")
    
    # 读取并处理2026年总收益数据
    if file_2026_total:
        print("\n5. 处理2026年总收益数据...")
        df_total = pd.read_excel(file_2026_total, sheet_name=0)
        
        platform_col = df_total.columns[3]   # 平台名称
        revenue_col = df_total.columns[8]    # 实得收益
        
        total_summary = df_total.groupby(platform_col)[revenue_col].sum()
        print(f"   总收益平台数: {len(total_summary)}")
        print(f"   总收益金额: {total_summary.sum():.2f}")
    
    # 读取并处理2025年收益数据
    if file_2025:
        print("\n6. 处理2025年收益数据...")
        df_2025 = pd.read_excel(file_2025, sheet_name=0)
        
        platform_col = df_2025.columns[3]   # 平台名称
        revenue_col = df_2025.columns[8]    # 实得收益
        
        summary_2025 = df_2025.groupby(platform_col)[revenue_col].sum()
        print(f"   2025年收益平台数: {len(summary_2025)}")
        print(f"   2025年总收益: {summary_2025.sum():.2f}")
    
    # 保存结果
    output_file = base_dir / "专区接入情况统计表_已整合.xlsx"
    df_stats.to_excel(output_file, index=False)
    print(f"\n7. 已保存到: {output_file}")
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)
    print("\n注意：由于统计表和收益文件的平台名称格式不同")
    print("（统计表使用代码如DQ_HuaSha，收益文件使用中文全称）")
    print("需要建立名称映射表才能正确匹配收益数据。")
    print("\n已添加以下列到统计表：")
    print("  - e交易26年3月_实得收益")
    print("  - e交易26年3月_当月收益")
    print("  - e交易26年3月_当月收益同比")
    print("  - e交易26年3月_当月收益环比")
    print("  - e交易26年_实得收益")
    print("  - e交易26年_26年总收益")
    print("  - e交易25年_实得收益")
    print("  - e交易25年_25年总收益")
    print("  - e交易总收益_实得收益")
    print("  - e交易总收益_总收益")
    print("  - e交易总收益_项目数")
    print("  - e交易总收益_总项目数")
    print("\n收益数据汇总：")
    if file_2026_month:
        print(f"  2026年3月总收益: {month_summary.sum():.2f} 元")
    if file_2026_total:
        print(f"  2026年总收益: {total_summary.sum():.2f} 元")
    if file_2025:
        print(f"  2025年总收益: {summary_2025.sum():.2f} 元")

if __name__ == "__main__":
    process_etrading_data()
