import pandas as pd
from datetime import datetime, timedelta

# 读取数据
df = pd.read_excel('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\e交易数据分析处理文件\\中原华北区专区数据_成本更新.xlsx')
df['确认接入时间'] = pd.to_datetime(df['确认接入时间'], errors='coerce')

current_date = pd.to_datetime('2026-04-08')
# 重新理解：接入超过3个月，小于1年
# 即：接入时间在 (当前日期-1年) 和 (当前日期-3个月) 之间
# 也就是：接入时间 > 1年前 且 接入时间 < 3个月前
one_year_ago = current_date - timedelta(days=365)  # 2025-04-08
three_months_ago = current_date - timedelta(days=90)  # 2026-01-08
half_year_ago = current_date - timedelta(days=180)  # 2025-10-10

print('=== 新指标计算 ===')
print()

# 原指标
print('【原指标】')
indicator1 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] == 0)])
print(f'指标一（接入超1年，总收益为0）: {indicator1}')

indicator2 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 100000)])
print(f'指标二（接入超1年，0<总收益<10w）: {indicator2}')

indicator3 = len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 50000)])
print(f'指标三（接入超1年，0<总收益<5w）: {indicator3}')

# 新指标四：接入超过3个月，小于1年，总收益为0
# 条件：接入时间在1年前到3个月前之间（即接入3个月-1年）且 总收益为0
# 接入时间 >= 1年前(2025-04-08) 且 接入时间 <= 3个月前(2026-01-08) 且 总收益=0
# 或者理解为：接入时间 > 1年前 且 接入时间 <= 3个月前
indicator4_new = len(df[(df['确认接入时间'] > one_year_ago) & (df['确认接入时间'] <= three_months_ago) & (df['总收益情况'] == 0)])
print(f'指标四（接入3个月-1年，总收益为0）: {indicator4_new}')

# 指标五
indicator5 = len(df[(df['确认接入时间'] < '2025-01-01') & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 50000)])
print(f'指标五（25年前接入，0<25年收益<5w）: {indicator5}')

# 指标六
indicator6 = len(df[df['26年收益情况'] > 0])
print(f'指标六（26年产生收益）: {indicator6}')

# 指标七
indicator7 = len(df[(df['25年收益情况'] > 0) & (df['26年收益情况'] == 0)])
print(f'指标七（25年有收益，26年无）: {indicator7}')

# 指标八
indicator8 = len(df[(df['确认接入时间'] < half_year_ago) & (df['总收益情况'] == 0)])
print(f'指标八（接入超半年，总收益为0）: {indicator8}')

print()
print('=== 验证指标四 ===')
print(f'计算条件: 确认接入时间 > {one_year_ago.strftime("%Y-%m-%d")} 且 <= {three_months_ago.strftime("%Y-%m-%d")} 且 总收益情况 = 0')

# 查看具体是哪些专区
print()
print('指标四涉及的专区:')
indicator4_df = df[(df['确认接入时间'] > one_year_ago) & (df['确认接入时间'] <= three_months_ago) & (df['总收益情况'] == 0)]
print(indicator4_df[['专区名称', '确认接入时间', '总收益情况']].to_string(index=False))
