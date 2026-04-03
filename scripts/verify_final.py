# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件/专区接入情况统计表_已整合_最终版.xlsx')
print('总行数:', len(df))
print('\n新增列:')
new_cols = [c for c in df.columns if 'e交易' in str(c)]
for col in new_cols:
    print(f'  - {col}')
print('\n有收益数据的平台数:', (df['e交易总收益_总收益'] > 0).sum())
print('\n前10条有收益的数据（包含总项目数）:')
print(df[df['e交易总收益_总收益'] > 0][['专区名称', 'e交易总收益_总收益', 'e交易总收益_总项目数']].head(10))
print('\n总项目数统计:')
print(f'  最大项目数: {df["e交易总收益_总项目数"].max()}')
has_projects = df[df["e交易总收益_总项目数"] > 0]
print(f'  最小项目数: {has_projects["e交易总收益_总项目数"].min()}')
print(f'  平均项目数: {has_projects["e交易总收益_总项目数"].mean():.2f}')
