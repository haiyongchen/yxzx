import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_excel('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\同步数据文件\\专区接入情况统计表_已整合_修正版.xlsx')

# 按省份分组统计e交易总收益
province_stats = df.groupby('省份')['e交易总收益_总收益'].sum().reset_index()
province_stats = province_stats.sort_values('e交易总收益_总收益', ascending=False)

# 创建图表
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(province_stats['省份'], province_stats['e交易总收益_总收益'], color='steelblue')

# 设置标题和标签
ax.set_xlabel('e交易总收益（元）', fontsize=12)
ax.set_ylabel('省份', fontsize=12)
ax.set_title('e交易专区收益统计 - 按省份分布', fontsize=14, fontweight='bold')

# 在柱状图上添加数值标签
for i, (idx, row) in enumerate(province_stats.iterrows()):
    value = row['e交易总收益_总收益']
    ax.text(value + 500000, i, f"{value:,.0f}", va='center', fontsize=9)

plt.tight_layout()
plt.savefig('D:\\openclaw-workspace\\province_chart.png', dpi=150, bbox_inches='tight')
print('图表已保存到: D:\\openclaw-workspace\\province_chart.png')

# 同时保存数据到Excel
province_stats.to_excel('D:\\openclaw-workspace\\province_stats_chart.xlsx', index=False, sheet_name='省份收益统计')
print('数据已保存到: D:\\openclaw-workspace\\province_stats_chart.xlsx')

# 打印统计信息
print('\n=== 统计结果 ===')
print(province_stats.to_string(index=False))
