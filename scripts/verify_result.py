# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件/专区接入情况统计表_已整合.xlsx')

print('总行数:', len(df))
print('\n新增列:')
new_cols = [c for c in df.columns if 'e交易' in str(c)]
for col in new_cols:
    print(f'  - {col}')

print('\n有收益数据的平台数:')
print(f'  26年3月: {(df["e交易26年3月_实得收益"] > 0).sum()}')
print(f'  26年总收益: {(df["e交易26年总收益_截至3月25日"] > 0).sum()}')
print(f'  25年总收益: {(df["e交易25年总收益"] > 0).sum()}')
print(f'  总收益: {(df["e交易总收益_截至2026年3月25日"] > 0).sum()}')

print('\n前5条有收益的数据:')
has_rev = df[df['e交易总收益_截至2026年3月25日'] > 0]
if len(has_rev) > 0:
    cols = ['交易平台', 'e交易26年3月_实得收益', 'e交易26年总收益_截至3月25日', 'e交易25年总收益', 'e交易总收益_截至2026年3月25日', 'e交易总项目数']
    print(has_rev[cols].head())
else:
    print("暂无有收益数据的平台")
