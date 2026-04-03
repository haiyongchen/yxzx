# -*- coding: utf-8 -*-
"""
处理e交易数据整合
根据专区接入情况统计表和e交易收益情况文件，整合数据
"""

import pandas as pd
import os
from pathlib import Path

def process_etrading_data():
    # 文件路径
    base_dir = Path("D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件")
    stats_file = base_dir / "专区接入情况统计表.xlsx"
    revenue_dir = base_dir / "e交易收益情况"
    
    print(f"读取统计表: {stats_file}")
    
    # 读取专区接入情况统计表
    df_stats = pd.read_excel(stats_file, sheet_name=0)
    
    # 显示前几行和列名，了解数据结构
    print("\n统计表列名:")
    print(df_stats.columns.tolist())
    print("\n统计表前5行:")
    print(df_stats.head())
    
    # 获取收益文件夹中的所有Excel文件
    revenue_files = list(revenue_dir.glob("*.xlsx"))
    print(f"\n找到 {len(revenue_files)} 个收益文件:")
    for f in revenue_files:
        print(f"  - {f.name}")
    
    # 读取所有收益数据并合并
    all_revenue_data = []
    for rev_file in revenue_files:
        print(f"\n读取: {rev_file.name}")
        try:
            df_rev = pd.read_excel(rev_file, sheet_name=0)
            print(f"  列名: {df_rev.columns.tolist()}")
            print(f"  行数: {len(df_rev)}")
            print(f"  前3行:\n{df_rev.head(3)}")
            all_revenue_data.append(df_rev)
        except Exception as e:
            print(f"  读取失败: {e}")
    
    # 合并所有收益数据
    if all_revenue_data:
        df_revenue = pd.concat(all_revenue_data, ignore_index=True)
        print(f"\n合并后收益数据总行数: {len(df_revenue)}")
        
        # 按平台名称分组并求和
        # 假设平台名称列叫'平台名称'或类似名称
        # 需要根据实际情况调整
        
        # 显示所有列名，找到平台名称列和收益列
        print("\n收益数据所有列名:")
        print(df_revenue.columns.tolist())
        
        # 保存处理后的数据
        output_file = base_dir / "专区接入情况统计表_已整合.xlsx"
        df_stats.to_excel(output_file, index=False)
        print(f"\n已保存到: {output_file}")
    else:
        print("\n没有读取到任何收益数据")

if __name__ == "__main__":
    process_etrading_data()
