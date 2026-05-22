import pandas as pd
import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 用openpyxl读取，保留合并单元格信息
file_path = r'D:\work\龙虾可操作需求临时文件夹\订单数据处理\阳光优采交易订单.xlsx'
wb = openpyxl.load_workbook(file_path)
ws = wb.active

print('=== 合并单元格信息 ===')
merged = list(ws.merged_cells.ranges)
print(f'合并单元格数量: {len(merged)}')
print()

# 显示前20个合并单元格
for i, m in enumerate(merged[:30]):
    print(f'  {m}')
print('...')
print()

# 查看第1-15行的数据
print('=== 前15行数据 ===')
for row in ws.iter_rows(min_row=1, max_row=15, values_only=False):
    row_data = []
    for cell in row:
        row_data.append(cell.value)
    print(f'行{row[0].row}: {row_data}')
