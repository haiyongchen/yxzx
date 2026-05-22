import pandas as pd
import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'D:\work\龙虾可操作需求临时文件夹\订单数据处理\阳光优采交易订单 (38).xlsx'
wb = openpyxl.load_workbook(file_path, read_only=True)
ws = wb.active

# 读取数据
data = []
headers = None
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        headers = list(row)
        continue
    data.append(list(row))

df = pd.DataFrame(data, columns=headers)

# 转换金额列为数值类型
df['订单金额（元）'] = pd.to_numeric(df['订单金额（元）'], errors='coerce')

print('=== 供应商类型分布 ===')
# 处理空值
df['供应商类型'] = df['供应商类型'].fillna('未填写')
print(df['供应商类型'].value_counts())
print()

# 按供应商类型统计订单数和金额
print('=== 按供应商类型统计 ===')
stats = df.groupby('供应商类型').agg(
    订单数=('订单号', 'count'),
    订单总金额=('订单金额（元）', 'sum')
).reset_index()

for _, row in stats.iterrows():
    supplier_type = row['供应商类型']
    count = row['订单数']
    amount = row['订单总金额']
    if pd.isna(amount):
        amount = 0
    print(f'{supplier_type}: {count} 单, 金额 {amount:,.2f} 元')

print()
total_count = len(df)
total_amount = df['订单金额（元）'].sum()
if pd.isna(total_amount):
    total_amount = 0
print(f'总计: {total_count} 单, 金额 {total_amount:,.2f} 元')

wb.close()
