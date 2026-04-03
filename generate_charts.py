# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import os

# 创建图表目录
chart_dir = 'D:\\openclaw-workspace\\charts'
os.makedirs(chart_dir, exist_ok=True)

print("正在生成可视化图表...")

# 图表1：成本收益趋势图
fig, ax = plt.subplots(figsize=(10, 6))
months = ['1月', '2月', '3月']
costs = [25000, 28000, 32000]
revenues = [15000, 35000, 66237]

ax.plot(months, costs, marker='o', linewidth=2, label='累计成本', color='#FF6B6B')
ax.plot(months, revenues, marker='s', linewidth=2, label='累计收益', color='#4ECDC4')
ax.axhline(y=32000, color='red', linestyle='--', label='成本基线(32,000元)')
ax.set_xlabel('月份', fontsize=12)
ax.set_ylabel('金额（元）', fontsize=12)
ax.set_title('成本收益趋势图', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{chart_dir}\\chart1_成本收益趋势.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表1: 成本收益趋势图")

# 图表2：成本率分布饼图
fig, ax = plt.subplots(figsize=(8, 8))
labels = ['<58%（健康）', '58%-65%（预警）', '>65%（超标）']
sizes = [10, 5, 4]
colors = ['#2ECC71', '#F39C12', '#E74C3C']
explode = (0.05, 0.05, 0.1)

ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', 
       startangle=90, textprops={'fontsize': 11})
ax.set_title('成本率分布', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{chart_dir}\\chart2_成本率分布.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表2: 成本率分布图")

# 图表3：问题专区分布柱状图
fig, ax = plt.subplots(figsize=(10, 6))
problems = ['接入超时', '项目数不达标', '收益不达标', '成本管控问题']
counts = [5, 3, 4, 2]
colors = ['#F1C40F', '#E67E22', '#E67E22', '#C0392B']

bars = ax.bar(problems, counts, color=colors, edgecolor='black', linewidth=1.2)
ax.set_ylabel('专区数量', fontsize=12)
ax.set_title('问题专区分布', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(counts) + 2)

# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}个',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(f'{chart_dir}\\chart3_问题专区分布.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表3: 问题专区分布图")

# 图表4：各省份成本对比柱状图
fig, ax = plt.subplots(figsize=(12, 6))
provinces = ['安徽', '北京', '河北', '河南', '湖北', '内蒙古', '山西', '陕西', '甘肃', '宁夏']
costs = [28000, 35000, 25000, 30000, 32000, 27000, 31000, 29000, 33000, 26000]
baseline = [32000] * len(provinces)

x = range(len(provinces))
width = 0.35

bars1 = ax.bar([i - width/2 for i in x], costs, width, label='实际成本', color='#3498DB', edgecolor='black')
ax.plot(x, baseline, 'r--', label='成本基线(32,000元)', linewidth=2)

ax.set_xlabel('省份', fontsize=12)
ax.set_ylabel('成本（元）', fontsize=12)
ax.set_title('各省份上线前成本对比', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(provinces, rotation=45)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{chart_dir}\\chart4_各省份成本对比.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表4: 各省份成本对比图")

# 图表5：成本率对比柱状图
fig, ax = plt.subplots(figsize=(12, 6))
provinces = ['安徽', '北京', '河北', '河南', '湖北', '内蒙古', '山西', '陕西', '甘肃', '宁夏']
cost_rates = [62, 117, 42, 55, 67, 52, 78, 50, 94, 40]
baseline_rate = [58] * len(provinces)

x = range(len(provinces))

# 根据成本率设置颜色
colors = []
for rate in cost_rates:
    if rate < 58:
        colors.append('#2ECC71')  # 绿色-健康
    elif rate <= 65:
        colors.append('#F39C12')  # 橙色-预警
    else:
        colors.append('#E74C3C')  # 红色-超标

bars = ax.bar(x, cost_rates, color=colors, edgecolor='black', linewidth=1.2)
ax.plot(x, baseline_rate, 'r--', label='成本率基线(58%)', linewidth=2)

ax.set_xlabel('省份', fontsize=12)
ax.set_ylabel('成本率（%）', fontsize=12)
ax.set_title('各省份成本率对比', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(provinces, rotation=45)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (bar, rate) in enumerate(zip(bars, cost_rates)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{rate}%',
            ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{chart_dir}\\chart5_各省份成本率对比.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表5: 各省份成本率对比图")

print(f"\n所有图表已生成完成！")
print(f"保存位置: {chart_dir}")
print("\n生成的图表列表：")
print("  1. chart1_成本收益趋势.png")
print("  2. chart2_成本率分布.png")
print("  3. chart3_问题专区分布.png")
print("  4. chart4_各省份成本对比.png")
print("  5. chart5_各省份成本率对比.png")
