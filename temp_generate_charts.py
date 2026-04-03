import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读取数据
file_path = 'D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\专区低收益统计结果.xlsx'
zhibiao1 = pd.read_excel(file_path, sheet_name='指标一-超1年总收益<10w')
zhibiao2 = pd.read_excel(file_path, sheet_name='指标二-25年前25年收益<10w')
zhibiao3 = pd.read_excel(file_path, sheet_name='指标三-超1年总收益<5w')
zhibiao4 = pd.read_excel(file_path, sheet_name='指标四-25年前25年收益<5w')
zhibiao5 = pd.read_excel(file_path, sheet_name='指标五-26年产生收益')
zhibiao6 = pd.read_excel(file_path, sheet_name='指标六-25年有收益26年无')

# 风险等级数据
risk_data = {
    '🔴 红色-重点关注': len(zhibiao1) + len(zhibiao3),  # 长期低收益
    '🟠 橙色-需改进': len(zhibiao2) + len(zhibiao4),    # 25年前收益不达标
    '🟡 黄色-观察': len(zhibiao5),                      # 26年有收益
    '⚪ 灰色-流失风险': len(zhibiao6)                   # 25年有但26年无
}

# 图1：风险等级分布饼图
fig1, ax1 = plt.subplots(figsize=(10, 8))
colors = ['#FF6B6B', '#FFA07A', '#FFD93D', '#95A5A6']
wedges, texts, autotexts = ax1.pie(risk_data.values(), labels=risk_data.keys(), autopct='%1.1f%%',
                                    colors=colors, startangle=90, textprops={'fontsize': 12})
ax1.set_title('e交易专区风险等级分布', fontsize=16, fontweight='bold', pad=20)
plt.setp(autotexts, size=11, weight='bold')
plt.tight_layout()
plt.savefig('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart1_risk_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('图1：风险等级分布饼图 - 已生成')

# 图2：收益区间分布（指标二数据）
revenue_bins = [0, 10000, 30000, 50000, 70000, 100000]
revenue_labels = ['0-1万', '1-3万', '3-5万', '5-7万', '7-10万']
zhibiao2['收益区间'] = pd.cut(zhibiao2['25年总收益'], bins=revenue_bins, labels=revenue_labels, right=False)
revenue_dist = zhibiao2['收益区间'].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
bars = ax2.bar(revenue_dist.index, revenue_dist.values, color='#4472C4', edgecolor='black', linewidth=1.2)
ax2.set_xlabel('25年总收益区间', fontsize=12)
ax2.set_ylabel('专区数量', fontsize=12)
ax2.set_title('25年前接入专区收益分布（25年总收益<10w）', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart2_revenue_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('图2：收益区间分布柱状图 - 已生成')

# 图3：TOP10重点关注专区（指标六 - 25年有但26年无）
fig3, ax3 = plt.subplots(figsize=(12, 6))
top10 = zhibiao6.nlargest(10, '25年总收益')[['专区号', '专区名称', '25年总收益']]
y_pos = range(len(top10))
bars = ax3.barh(y_pos, top10['25年总收益'].values, color='#E74C3C', edgecolor='black', linewidth=1)
ax3.set_yticks(y_pos)
ax3.set_yticklabels([f"{row['专区号']}\n{row['专区名称'][:15]}" for _, row in top10.iterrows()], fontsize=9)
ax3.invert_yaxis()
ax3.set_xlabel('25年总收益（元）', fontsize=12)
ax3.set_title('⚠️ TOP10 流失风险专区（25年有收益但26年无）', fontsize=14, fontweight='bold', color='#E74C3C')
ax3.grid(axis='x', alpha=0.3)
# 添加数值标签
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax3.text(width, bar.get_y() + bar.get_height()/2.,
             f'{int(width):,}',
             ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart3_top10_risk.png', dpi=150, bbox_inches='tight')
plt.close()
print('图3：TOP10流失风险专区 - 已生成')

# 图4：各指标数量对比
fig4, ax4 = plt.subplots(figsize=(12, 6))
metrics = ['指标一\n(超1年收益<10w)', '指标二\n(25年前收益<10w)', '指标三\n(超1年收益<5w)', 
           '指标四\n(25年前收益<5w)', '指标五\n(26年有收益)', '指标六\n(25有26无)']
counts = [len(zhibiao1), len(zhibiao2), len(zhibiao3), len(zhibiao4), len(zhibiao5), len(zhibiao6)]
colors_bar = ['#FF6B6B', '#FFA07A', '#FF6B6B', '#FFA07A', '#FFD93D', '#95A5A6']
bars = ax4.bar(metrics, counts, color=colors_bar, edgecolor='black', linewidth=1.2)
ax4.set_ylabel('专区数量', fontsize=12)
ax4.set_title('六大指标专区数量统计', fontsize=14, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart4_metrics_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print('图4：六大指标对比图 - 已生成')

print('\n✅ 所有图表生成完成！')
print('图表保存路径: D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\')
