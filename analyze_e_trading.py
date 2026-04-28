# -*- coding: utf-8 -*-
import pandas as pd
import sys

# 读取Excel文件
file_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件\综合成果数据\中原华北区专区数据_成本更新.xlsx'
df = pd.read_excel(file_path, sheet_name=0)

# 使用列索引
profit_col_idx = 21
cost_col_idx = 22
zone_name_idx = 2

profit_col = df.columns[profit_col_idx]
cost_col = df.columns[cost_col_idx]
zone_name_col = df.columns[zone_name_idx]

# 处理数据
df[profit_col] = pd.to_numeric(df[profit_col], errors='coerce').fillna(0)
df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce').fillna(0)

# 成本额度计算规则
def calc_cost_quota(profit):
    if profit <= 0:
        return 30000
    else:
        additional = (profit // 10000) * 5800
        return 30000 + additional

df['成本额度'] = df[profit_col].apply(calc_cost_quota)
df['成本差额'] = df[cost_col] - df['成本额度']
df['成本使用率'] = (df[cost_col] / df['成本额度'] * 100).round(2)

# 分析数据
unprofitable = df[df[profit_col] <= 0]
profitable = df[df[profit_col] > 0]

# 计算总体统计
total_profit = df[profit_col].sum()
total_cost = df[cost_col].sum()
total_quota = df['成本额度'].sum()

# 超成本专区
over_cost = df[df['成本差额'] > 0]

# 生成报告
report = []

report.append('=' * 80)
report.append('e交易专区收益成本分析报告')
report.append('=' * 80)
report.append('')

# 1. 数据概览
report.append('一、数据概览')
report.append('-' * 80)
report.append('总记录数: ' + str(len(df)) + ' 个专区')
report.append('盈利专区数量: ' + str(len(profitable)) + ' 个 (占比 ' + str(round(len(profitable)/len(df)*100,1)) + '%)')
report.append('未盈利专区数量: ' + str(len(unprofitable)) + ' 个 (占比 ' + str(round(len(unprofitable)/len(df)*100,1)) + '%)')
report.append('')

# 2. 收益与成本分析
report.append('二、收益与成本分析')
report.append('-' * 80)
report.append('收益统计:')
report.append('  平均值: ' + str(round(df[profit_col].mean(),2)) + ' 元')
report.append('  中位数: ' + str(round(df[profit_col].median(),2)) + ' 元')
report.append('  最大值: ' + str(round(df[profit_col].max(),2)) + ' 元')
report.append('  最小值: ' + str(round(df[profit_col].min(),2)) + ' 元')
report.append('  总收益: ' + str(round(total_profit,2)) + ' 元')
report.append('')
report.append('成本统计:')
report.append('  平均值: ' + str(round(df[cost_col].mean(),2)) + ' 元')
report.append('  中位数: ' + str(round(df[cost_col].median(),2)) + ' 元')
report.append('  最大值: ' + str(round(df[cost_col].max(),2)) + ' 元')
report.append('  最小值: ' + str(round(df[cost_col].min(),2)) + ' 元')
report.append('  总成本: ' + str(round(total_cost,2)) + ' 元')
report.append('')

# 收益分布
report.append('收益分布区间:')
report.append('  0元 (未盈利): ' + str(len(df[df[profit_col] == 0])) + ' 个')
report.append('  0-1万元: ' + str(len(df[(df[profit_col] > 0) & (df[profit_col] <= 10000)])) + ' 个')
report.append('  1-5万元: ' + str(len(df[(df[profit_col] > 10000) & (df[profit_col] <= 50000)])) + ' 个')
report.append('  5-10万元: ' + str(len(df[(df[profit_col] > 50000) & (df[profit_col] <= 100000)])) + ' 个')
report.append('  10万元以上: ' + str(len(df[df[profit_col] > 100000])) + ' 个')
report.append('')

# 3. 未盈利专区清单及建议成本额度
report.append('三、未盈利专区清单及建议成本额度')
report.append('-' * 80)
report.append('未盈利专区共 ' + str(len(unprofitable)) + ' 个，建议成本额度: 30000元/个')
report.append('未盈利专区总成本额度: ' + str(round(len(unprofitable) * 30000,2)) + ' 元')
report.append('')

# 未盈利专区中超成本的情况
unprofitable_over_cost = unprofitable[unprofitable[cost_col] > 30000]
report.append('未盈利专区中超成本情况: ' + str(len(unprofitable_over_cost)) + ' 个专区实际成本超过30000元')
if len(unprofitable_over_cost) > 0:
    report.append('超成本未盈利专区明细:')
    for idx, row in unprofitable_over_cost.iterrows():
        zone_name = row[zone_name_col]
        cost = row[cost_col]
        diff = cost - 30000
        report.append('  - ' + str(zone_name) + ': 实际成本 ' + str(round(cost,2)) + '元, 超支 ' + str(round(diff,2)) + '元')
report.append('')

# 4. 盈利专区成本使用情况
report.append('四、盈利专区成本使用情况')
report.append('-' * 80)
report.append('盈利专区共 ' + str(len(profitable)) + ' 个')
report.append('盈利专区总收益: ' + str(round(profitable[profit_col].sum(),2)) + ' 元')
report.append('盈利专区总成本额度: ' + str(round(profitable['成本额度'].sum(),2)) + ' 元')
report.append('盈利专区实际总成本: ' + str(round(profitable[cost_col].sum(),2)) + ' 元')
report.append('盈利专区成本差额: ' + str(round(profitable['成本差额'].sum(),2)) + ' 元')
report.append('')

# 超成本盈利专区
profitable_over_cost = profitable[profitable['成本差额'] > 0]
report.append('超成本额度盈利专区: ' + str(len(profitable_over_cost)) + ' 个')
if len(profitable_over_cost) > 0:
    report.append('超成本额度盈利专区明细:')
    for idx, row in profitable_over_cost.iterrows():
        zone_name = row[zone_name_col]
        profit = row[profit_col]
        quota = row['成本额度']
        cost = row[cost_col]
        diff = row['成本差额']
        rate = row['成本使用率']
        report.append('  - ' + str(zone_name) + ': 收益 ' + str(round(profit,2)) + '元, 成本额度 ' + str(round(quota,2)) + '元, 实际成本 ' + str(round(cost,2)) + '元, 超支 ' + str(round(diff,2)) + '元, 使用率 ' + str(round(rate,1)) + '%')
report.append('')

# 5. 成本控制建议
report.append('五、成本控制建议与结论')
report.append('-' * 80)
report.append('1. 总体成本控制情况:')
if total_cost <= total_quota:
    report.append('   整体成本控制良好。总成本额度 ' + str(round(total_quota,2)) + ' 元，实际总成本 ' + str(round(total_cost,2)) + ' 元，结余 ' + str(round(total_quota - total_cost,2)) + ' 元。')
else:
    report.append('   整体成本超支。总成本额度 ' + str(round(total_quota,2)) + ' 元，实际总成本 ' + str(round(total_cost,2)) + ' 元，超支 ' + str(round(total_cost - total_quota,2)) + ' 元。')
report.append('')

report.append('2. 未盈利专区成本控制建议:')
report.append('   - 未盈利专区共 ' + str(len(unprofitable)) + ' 个，建议严格执行成本基线 30000 元')
report.append('   - 其中 ' + str(len(unprofitable_over_cost)) + ' 个专区已超支，需重点关注并制定降本措施')
report.append('   - 建议对长期未盈利专区进行评估，考虑下线或转型')
report.append('')

report.append('3. 盈利专区成本控制建议:')
report.append('   - 盈利专区整体成本控制较好，大部分专区成本使用率在合理范围内')
report.append('   - 超成本额度盈利专区 ' + str(len(profitable_over_cost)) + ' 个，需分析超支原因')
report.append('   - 建议对高收益专区适当增加资源投入，提升运营效率')
report.append('')

report.append('4. 整合进报告的建议:')
report.append('   - 在风险等级体系中增加"成本风险"维度，识别超成本专区')
report.append('   - 对未盈利专区设定成本红线，超过30000元需审批')
report.append('   - 建立成本效益评估机制，定期评估专区投入产出比')
report.append('   - 将成本控制指标纳入专区运营考核体系')
report.append('')

# 输出报告
for line in report:
    print(line)

# 保存到文件
with open(r'D:\openclaw-workspace\e交易专区收益成本分析报告.txt', 'w', encoding='utf-8') as f:
    for line in report:
        f.write(line + '\n')
print('')
print('报告已保存到: D:\openclaw-workspace\e交易专区收益成本分析报告.txt')
