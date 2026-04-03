# -*- coding: utf-8 -*-
import pandas as pd

print('小橘分析26年度新开设专区...')

# 读取数据
df_c = pd.read_csv('D:\\openclaw-workspace\\all_zones_c_contract.csv', encoding='utf-8-sig')

# 数据处理
df_c['总收益情况'] = pd.to_numeric(df_c['总收益情况'], errors='coerce').fillna(0)
df_c['上线前成本'] = pd.to_numeric(df_c['上线前成本'], errors='coerce').fillna(0)
df_c['专区成本'] = pd.to_numeric(df_c['专区成本'], errors='coerce').fillna(0)

# 注意：专区成本已包含上线前成本，使用专区成本作为总成本
df_c['总成本'] = df_c['专区成本']

# 处理时间字段
df_c['确认接入时间'] = pd.to_datetime(df_c['确认接入时间'], errors='coerce')
df_c['接入年份'] = df_c['确认接入时间'].dt.year

# 筛选26年度新开设专区（2026年接入）
df_2026 = df_c[df_c['接入年份'] == 2026].copy()

print('=== 26年度新开设专区统计 ===')
print(f'26年度新开设专区数量: {len(df_2026)}')
print()

if len(df_2026) > 0:
    print('=== 26年度新开设专区列表 ===')
    display_cols = ['合同编号', ' 原专区名称', '所属省份', '确认接入时间', '专区成本', '总收益情况']
    print(df_2026[display_cols].to_string())
    print()
    
    print('=== 26年度新开设专区成本统计 ===')
    print(f'总成本: {df_2026["专区成本"].sum():,.2f} 元')
    print(f'平均成本: {df_2026["专区成本"].mean():,.2f} 元')
    print(f'成本中位数: {df_2026["专区成本"].median():,.2f} 元')
    print(f'最高成本: {df_2026["专区成本"].max():,.2f} 元')
    print(f'最低成本: {df_2026["专区成本"].min():,.2f} 元')
    print()
    
    print('=== 26年度新开设专区收益统计 ===')
    print(f'总收益: {df_2026["总收益情况"].sum():,.2f} 元')
    print(f'平均收益: {df_2026["总收益情况"].mean():,.2f} 元')
    print()
    
    # 成本分布
    print('=== 26年度新开设专区成本分布 ===')
    high_cost = df_2026[df_2026['专区成本'] > 32000]
    medium_cost = df_2026[(df_2026['专区成本'] > 10000) & (df_2026['专区成本'] <= 32000)]
    low_cost = df_2026[df_2026['专区成本'] <= 10000]
    
    print(f'高成本专区(>32000): {len(high_cost)} 个')
    print(f'中成本专区(10000-32000): {len(medium_cost)} 个')
    print(f'低成本专区(<=10000): {len(low_cost)} 个')
    
    if len(high_cost) > 0:
        print()
        print('=== 高成本专区详情 ===')
        print(high_cost[[' 原专区名称', '所属省份', '专区成本']].to_string())
    
    # 保存26年度数据
    df_2026.to_csv('D:\\openclaw-workspace\\zones_2026.csv', index=False, encoding='utf-8-sig')
    print()
    print('✅ 26年度数据已保存')
else:
    print('⚠️ 没有找到26年度新开设的专区')
