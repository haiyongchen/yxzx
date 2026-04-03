#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查各指标是否包含收益为0的数据
"""

import pandas as pd
from datetime import datetime

# 读取原始数据
file_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\temp\专区信息汇总表_中原华北_合并.xlsx'
df = pd.read_excel(file_path)

# 获取关键列
confirm_time = df.iloc[:, 14]  # 确认接入时间
total_revenue = df.iloc[:, 21] # 总收益
revenue_25 = df.iloc[:, 19]    # 25年总收益

# 当前日期
current_date = datetime(2026, 4, 2)
one_year_ago = datetime(2025, 4, 2)
year_2025_start = datetime(2025, 1, 1)

# 清理数据
confirm_time_clean = pd.to_datetime(confirm_time, errors='coerce')
total_revenue_clean = pd.to_numeric(total_revenue, errors='coerce')
revenue_25_clean = pd.to_numeric(revenue_25, errors='coerce')

# 指标一：超1年且总收益<10w
condition1 = (confirm_time_clean < one_year_ago) & (total_revenue_clean < 100000) & (total_revenue_clean.notna())
zhibiao1 = df[condition1]

# 指标二：25年前且25年收益<10w
condition2 = (confirm_time_clean < year_2025_start) & (revenue_25_clean < 100000) & (revenue_25_clean.notna())
zhibiao2 = df[condition2]

# 指标三：超1年且总收益<5w
condition3 = (confirm_time_clean < one_year_ago) & (total_revenue_clean < 50000) & (total_revenue_clean.notna())
zhibiao3 = df[condition3]

# 指标四：25年前且25年收益<5w
condition4 = (confirm_time_clean < year_2025_start) & (revenue_25_clean < 50000) & (revenue_25_clean.notna())
zhibiao4 = df[condition4]

# 新指标七：超1年且总收益为0
condition7 = (confirm_time_clean < one_year_ago) & ((total_revenue_clean == 0) | (total_revenue_clean.isna()))
zhibiao7 = df[condition7]

print('=== 检查结果 ===')
print(f'指标一（超1年总收益<10w）: {len(zhibiao1)}个')
zhibiao1_revenue = pd.to_numeric(zhibiao1.iloc[:, 21], errors='coerce')
zhibiao1_zero = (zhibiao1_revenue == 0).sum()
print(f'  - 其中收益为0的: {zhibiao1_zero}个')
print()

print(f'指标二（25年前25年收益<10w）: {len(zhibiao2)}个')
zhibiao2_revenue = pd.to_numeric(zhibiao2.iloc[:, 19], errors='coerce')
zhibiao2_zero = (zhibiao2_revenue == 0).sum()
print(f'  - 其中25年收益为0的: {zhibiao2_zero}个')
print()

print(f'指标三（超1年总收益<5w）: {len(zhibiao3)}个')
zhibiao3_revenue = pd.to_numeric(zhibiao3.iloc[:, 21], errors='coerce')
zhibiao3_zero = (zhibiao3_revenue == 0).sum()
print(f'  - 其中收益为0的: {zhibiao3_zero}个')
print()

print(f'指标四（25年前25年收益<5w）: {len(zhibiao4)}个')
zhibiao4_revenue = pd.to_numeric(zhibiao4.iloc[:, 19], errors='coerce')
zhibiao4_zero = (zhibiao4_revenue == 0).sum()
print(f'  - 其中25年收益为0的: {zhibiao4_zero}个')
print()

print(f'指标七（超1年总收益为0）: {len(zhibiao7)}个')
print()

# 检查指标三和指标七的关系
zhibiao3_set = set(zhibiao3.iloc[:, 1].dropna())
zhibiao7_set = set(zhibiao7.iloc[:, 1].dropna())
print('=== 指标三和指标七的关系 ===')
print(f'指标七是否属于指标三的子集: {zhibiao7_set.issubset(zhibiao3_set)}')
print(f'指标三包含指标七的数量: {len(zhibiao7_set.intersection(zhibiao3_set))} / {len(zhibiao7_set)}')
print()

# 分析：指标三 = 0收益 + (0,5w)收益
zhibiao3_positive = zhibiao3_revenue[(zhibiao3_revenue > 0) & (zhibiao3_revenue < 50000)]
print('=== 指标三细分 ===')
print(f'指标三总数: {len(zhibiao3)}')
print(f'  - 收益为0: {zhibiao3_zero}个')
print(f'  - 收益在(0,5w)之间: {len(zhibiao3_positive)}个')
print(f'  验证: {zhibiao3_zero} + {len(zhibiao3_positive)} = {zhibiao3_zero + len(zhibiao3_positive)}')
