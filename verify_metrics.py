#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证各指标数量
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
revenue_26 = df.iloc[:, 20]    # 26年总收益

# 当前日期
current_date = datetime(2026, 4, 2)
one_year_ago = datetime(2025, 4, 2)
year_2025_start = datetime(2025, 1, 1)

# 清理数据
confirm_time_clean = pd.to_datetime(confirm_time, errors='coerce')
total_revenue_clean = pd.to_numeric(total_revenue, errors='coerce')
revenue_25_clean = pd.to_numeric(revenue_25, errors='coerce')
revenue_26_clean = pd.to_numeric(revenue_26, errors='coerce')

print('=== 验证各指标数量 ===')
print()

# 指标一：接入超过1年，总收益为0
condition1 = (confirm_time_clean < one_year_ago) & ((total_revenue_clean == 0) | (total_revenue_clean.isna()))
count1 = condition1.sum()
print(f'指标一：接入超过1年，总收益为0')
print(f'  条件：confirm_time < 2025-04-02 AND (total_revenue == 0 OR isna)')
print(f'  数量：{count1}')
print()

# 指标二：接入超过1年，0<总收益<10w
condition2 = (confirm_time_clean < one_year_ago) & (total_revenue_clean > 0) & (total_revenue_clean < 100000)
count2 = condition2.sum()
print(f'指标二：接入超过1年，0<总收益<10w')
print(f'  条件：confirm_time < 2025-04-02 AND total_revenue > 0 AND total_revenue < 100000')
print(f'  数量：{count2}')
print()

# 指标三：25年前接入，0<25年收益<10w
condition3 = (confirm_time_clean < year_2025_start) & (revenue_25_clean > 0) & (revenue_25_clean < 100000)
count3 = condition3.sum()
print(f'指标三：25年前接入，0<25年收益<10w')
print(f'  条件：confirm_time < 2025-01-01 AND revenue_25 > 0 AND revenue_25 < 100000')
print(f'  数量：{count3}')
print()

# 指标四：接入超过1年，0<总收益<5w
condition4 = (confirm_time_clean < one_year_ago) & (total_revenue_clean > 0) & (total_revenue_clean < 50000)
count4 = condition4.sum()
print(f'指标四：接入超过1年，0<总收益<5w')
print(f'  条件：confirm_time < 2025-04-02 AND total_revenue > 0 AND total_revenue < 50000')
print(f'  数量：{count4}')
print()

# 指标五：25年前接入，0<25年收益<5w
condition5 = (confirm_time_clean < year_2025_start) & (revenue_25_clean > 0) & (revenue_25_clean < 50000)
count5 = condition5.sum()
print(f'指标五：25年前接入，0<25年收益<5w')
print(f'  条件：confirm_time < 2025-01-01 AND revenue_25 > 0 AND revenue_25 < 50000')
print(f'  数量：{count5}')
print()

# 指标六：26年产生收益
condition6 = (revenue_26_clean > 0) & (revenue_26_clean.notna())
count6 = condition6.sum()
print(f'指标六：26年产生收益')
print(f'  条件：revenue_26 > 0 AND notna')
print(f'  数量：{count6}')
print()

# 指标七：25年有收益，26年无
condition7 = (revenue_25_clean > 0) & (revenue_25_clean.notna()) & ((revenue_26_clean == 0) | (revenue_26_clean.isna()))
count7 = condition7.sum()
print(f'指标七：25年有收益，26年无')
print(f'  条件：revenue_25 > 0 AND notna AND (revenue_26 == 0 OR isna)')
print(f'  数量：{count7}')
print()

# 验证包含关系
print('=== 验证包含关系 ===')
print()

# 指标四应该是指标二的子集
zhibiao2_set = set(df[condition2].iloc[:, 1].dropna())
zhibiao4_set = set(df[condition4].iloc[:, 1].dropna())
print(f'指标四是否属于指标二的子集: {zhibiao4_set.issubset(zhibiao2_set)}')
print(f'指标四在指标二中的比例: {len(zhibiao4_set)} / {len(zhibiao2_set)}')
print()

# 指标五应该是指标三的子集
zhibiao3_set = set(df[condition3].iloc[:, 1].dropna())
zhibiao5_set = set(df[condition5].iloc[:, 1].dropna())
print(f'指标五是否属于指标三的子集: {zhibiao5_set.issubset(zhibiao3_set)}')
print(f'指标五在指标三中的比例: {len(zhibiao5_set)} / {len(zhibiao3_set)}')
print()

# 检查指标一和指标四是否有重叠
zhibiao1_set = set(df[condition1].iloc[:, 1].dropna())
overlap_1_4 = zhibiao1_set.intersection(zhibiao4_set)
print(f'指标一和指标四重叠数量: {len(overlap_1_4)} (应该为0)')
print()

# 检查指标二和指标四的关系
overlap_2_4 = zhibiao2_set.intersection(zhibiao4_set)
print(f'指标二和指标四重叠数量: {len(overlap_2_4)} (应该等于指标四)')
