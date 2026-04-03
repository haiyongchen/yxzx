import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

# 读取所有sheet
file_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\temp\专区信息汇总表_中原华北.xlsx'
all_sheets = pd.read_excel(file_path, sheet_name=None)

print('开始合并以下sheet:')
all_data = []
for sheet_name, df in all_sheets.items():
    print(f'  - {sheet_name}: {len(df)} 行')
    # 添加来源sheet列
    df['来源Sheet'] = sheet_name
    all_data.append(df)

# 合并所有数据
merged_df = pd.concat(all_data, ignore_index=True)
print(f'\n合并完成！总行数: {len(merged_df)}')

# 保存到新的Excel文件
output_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\temp\专区信息汇总表_中原华北_合并.xlsx'
merged_df.to_excel(output_path, index=False, sheet_name='合并数据')

print(f'\n已保存到: {output_path}')
