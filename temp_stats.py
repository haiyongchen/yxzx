import pandas as pd
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel(r'C:\Users\63111\Desktop\阳光优采交易订单.xlsx')
df['订单日期'] = pd.to_datetime(df['订单日期'])
df['订单金额（元）'] = pd.to_numeric(df['订单金额（元）'], errors='coerce')

now = datetime(2026, 5, 18)
week_start = datetime(2026, 5, 12, 0, 0, 0)
week_end = datetime(2026, 5, 18, 23, 59, 59)
month_start = datetime(2026, 5, 1, 0, 0, 0)

# 本月统计
df_month = df[df['订单日期'] >= month_start]
month_stats = df_month.groupby('专区名称').agg(
    订单数=('订单号', 'count'),
    订单总金额=('订单金额（元）', 'sum')
).reset_index()
month_stats = month_stats.sort_values('订单数', ascending=False)
month_stats.loc[len(month_stats)] = ['合计', month_stats['订单数'].sum(), month_stats['订单总金额'].sum()]

# 本周统计
df_week = df[(df['订单日期'] >= week_start) & (df['订单日期'] <= week_end)]
week_stats = df_week.groupby('专区名称').agg(
    订单数=('订单号', 'count'),
    订单总金额=('订单金额（元）', 'sum')
).reset_index()
week_stats = week_stats.sort_values('订单数', ascending=False)
week_stats.loc[len(week_stats)] = ['合计', week_stats['订单数'].sum(), week_stats['订单总金额'].sum()]

# 写入Excel
output_path = r'C:\Users\63111\Desktop\阳光优采订单统计.xlsx'
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    month_stats.to_excel(writer, sheet_name='本月订单统计', index=False)
    week_stats.to_excel(writer, sheet_name='本周订单统计', index=False)

print(f'文件已保存到: {output_path}')
