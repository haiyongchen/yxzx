import pandas as pd
import sys
from datetime import datetime, timedelta

# 读取数据
df = pd.read_excel('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\e交易数据分析处理文件\\中原华北区专区数据_成本更新.xlsx')

# 转换日期
df['确认接入时间'] = pd.to_datetime(df['确认接入时间'], errors='coerce')

# 当前日期（使用2026-04-08作为当前日期）
current_date = pd.to_datetime('2026-04-08')
half_year_ago = current_date - timedelta(days=180)

print('=== 数据验证与统计 ===')
print(f'总专区数: {len(df)}')
print()

# 原有指标验证
print('【原有指标验证】')
indicator1 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] == 0)])
print(f'指标一（接入超1年，总收益为0）: {indicator1}')

indicator2 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 100000)])
print(f'指标二（接入超1年，0<总收益<10w）: {indicator2}')

indicator3 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 50000)])
print(f'指标三（接入超1年，0<总收益<5w）: {indicator3}')

indicator4 = len(df[(df['确认接入时间'] < '2025-01-01') & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 100000)])
print(f'指标四（25年前接入，0<25年收益<10w）: {indicator4}')

indicator5 = len(df[(df['确认接入时间'] < '2025-01-01') & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 50000)])
print(f'指标五（25年前接入，0<25年收益<5w）: {indicator5}')

indicator6 = len(df[df['26年收益情况'] > 0])
print(f'指标六（26年产生收益）: {indicator6}')

indicator7 = len(df[(df['25年收益情况'] > 0) & (df['26年收益情况'] == 0)])
print(f'指标七（25年有收益，26年无）: {indicator7}')

print()
print('【新增指标】')
# 新指标：确认接入时间距今半年无收益
indicator8 = len(df[(df['确认接入时间'] < half_year_ago) & (df['总收益情况'] == 0)])
print(f'指标八（接入超半年，总收益为0）: {indicator8}')
print(f'  计算条件: 确认接入时间 < {half_year_ago.strftime("%Y-%m-%d")} 且 总收益情况 = 0')

print()
print('=== 数据样本验证 ===')
print('接入超半年且零收益的专区示例:')
sample = df[(df['确认接入时间'] < half_year_ago) & (df['总收益情况'] == 0)][['专区名称', '确认接入时间', '总收益情况']].head(5)
print(sample.to_string(index=False))
