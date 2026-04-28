---
name: e-trading-zone-profit-second
description: e交易数据处理 - 专区收益二次匹配处理。针对收益为0的行（黄色标记），根据专区名称与合并表进行二次匹配，匹配成功的行填充淡蓝色背景。Use when 用户需要对e交易专区收益数据进行二次匹配、补充匹配黄色标记行、更新未匹配数据。
---

# 专区收益二次匹配 Skill

用于e交易数据处理中，对收益为0的行进行二次匹配补充。

## 使用场景

- 处理中原华北区专区数据_已更新.xlsx 中收益为0的行
- 根据专区信息汇总表_中原华北_合并.xlsx 进行二次匹配
- 按"专区名称"匹配，更新25年、26年、总收益数据
- 匹配成功的行填充淡蓝色背景

## 匹配规则

1. **匹配字段**:
   - 目标文件（中原华北区专区数据_已更新.xlsx）:
     - C列: 专区名称
     - R列: 25年收益情况
     - S列: 26年收益情况
     - T列: 总收益情况
   - 合并文件（专区信息汇总表_中原华北_合并.xlsx）:
     - C列: 专区名称
     - T列: 25年总收益
     - U列: 26年总收益
     - V列: 总收益

2. **匹配条件**:
   - 只匹配目标文件中收益都为0的行（黄色标记行）
   - 合并文件中T、U、V列至少有一列不为0才参与匹配
   - 按"专区名称"精确匹配

3. **结果处理**:
   - 匹配成功: 更新R、S、T列数据，整行填充淡蓝色
   - 匹配失败: 保持原样（仍为黄色）

## 处理流程

1. 读取目标文件和合并文件
2. 找到目标文件中收益都为0的行（黄色标记行）
3. 构建合并文件的匹配字典（只包含有数据的）
4. 遍历黄色行，按专区名称匹配
5. 匹配成功的更新数据并记录行号
6. 保存数据到原文件
7. 对匹配成功的行填充淡蓝色背景

## Python 处理代码

```python
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def to_float(val):
    """转换为float，失败返回0"""
    if pd.isna(val):
        return 0
    try:
        return float(val)
    except:
        return 0

# 文件路径
base_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件'
target_file = os.path.join(base_path, '中原华北区专区数据_已更新.xlsx')
merge_file = os.path.join(base_path, '专区信息汇总表_中原华北_合并.xlsx')

# 读取文件
df_target = pd.read_excel(target_file)
df_merge = pd.read_excel(merge_file)

# 获取列名
target_cols = df_target.columns.tolist()
merge_cols = df_merge.columns.tolist()

# 关键列
zhuanqu_name_col_target = target_cols[2]   # C列: 专区名称
zhuanqu_name_col_merge = merge_cols[2]     # C列: 专区名称
col_25_target = target_cols[17]            # R列: 25年收益情况
col_26_target = target_cols[18]            # S列: 26年收益情况
col_total_target = target_cols[19]         # T列: 总收益情况
col_25_merge = merge_cols[19]              # T列: 25年总收益
col_26_merge = merge_cols[20]              # U列: 26年总收益
col_total_merge = merge_cols[21]           # V列: 总收益

# 确保目标文件的收益列为float类型
df_target[col_25_target] = df_target[col_25_target].apply(to_float)
df_target[col_26_target] = df_target[col_26_target].apply(to_float)
df_target[col_total_target] = df_target[col_total_target].apply(to_float)

# 找到当前收益都为0的行（黄色标记的）
yellow_rows = []
for idx, row in df_target.iterrows():
    val_25 = row[col_25_target]
    val_26 = row[col_26_target]
    val_total = row[col_total_target]
    
    is_zero = (val_25 == 0) and (val_26 == 0) and (val_total == 0)
    
    if is_zero:
        yellow_rows.append(idx)

print(f'当前收益为0的行数: {len(yellow_rows)}')

# 构建合并文件的匹配字典（只包含有数据的）
merge_dict = {}
for idx, row in df_merge.iterrows():
    name = str(row[zhuanqu_name_col_merge]).strip() if pd.notna(row[zhuanqu_name_col_merge]) else ''
    val_25 = to_float(row[col_25_merge])
    val_26 = to_float(row[col_26_merge])
    val_total = to_float(row[col_total_merge])
    
    # 检查T、U、V列是否存在不为0的数据
    if name and (val_25 != 0 or val_26 != 0 or val_total != 0):
        merge_dict[name] = {
            '25年': val_25,
            '26年': val_26,
            '总收益': val_total
        }

print(f'合并文件有效数据: {len(merge_dict)} 条')

# 二次匹配：对黄色行进行匹配
matched_count = 0
matched_rows = []  # 记录匹配成功的行号

for idx in yellow_rows:
    name = str(df_target.at[idx, zhuanqu_name_col_target]).strip() if pd.notna(df_target.at[idx, zhuanqu_name_col_target]) else ''
    
    if name in merge_dict:
        # 更新数据
        df_target.at[idx, col_25_target] = merge_dict[name]['25年']
        df_target.at[idx, col_26_target] = merge_dict[name]['26年']
        df_target.at[idx, col_total_target] = merge_dict[name]['总收益']
        matched_count += 1
        matched_rows.append(idx)

print(f'二次匹配成功: {matched_count} 条')
print(f'仍未匹配: {len(yellow_rows) - matched_count} 条')

# 保存数据
df_target.to_excel(target_file, index=False)
print(f'数据已保存')

# 分类行
yellow_rows = []      # 收益为0的行
light_blue_rows = []  # 收益不为0的行

for idx, row in df_target.iterrows():
    val_25 = to_float(row[col_25_target])
    val_26 = to_float(row[col_26_target])
    val_total = to_float(row[col_total_target])
    
    is_zero = (val_25 == 0) and (val_26 == 0) and (val_total == 0)
    
    if is_zero:
        yellow_rows.append(idx)
    else:
        light_blue_rows.append(idx)

# 使用openpyxl填充颜色
wb = load_workbook(target_file)
ws = wb.active

# 定义颜色
yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
light_blue_fill = PatternFill(start_color='ADD8E6', end_color='ADD8E6', fill_type='solid')

# 先对所有数据行清除填充（保留表头）
for row in range(2, ws.max_row + 1):
    for col in range(1, ws.max_column + 1):
        ws.cell(row=row, column=col).fill = PatternFill(fill_type=None)

# 对收益为0的行填充黄色
for row_idx in yellow_rows:
    excel_row = row_idx + 2
    for col in range(1, ws.max_column + 1):
        ws.cell(row=excel_row, column=col).fill = yellow_fill

# 对收益不为0的行填充淡蓝色
for row_idx in light_blue_rows:
    excel_row = row_idx + 2
    for col in range(1, ws.max_column + 1):
        ws.cell(row=excel_row, column=col).fill = light_blue_fill

wb.save(target_file)
print(f'颜色填充完成：')
print(f'  - 黄色: {len(yellow_rows)} 行（收益为0）')
print(f'  - 淡蓝色: {len(light_blue_rows)} 行（收益不为0）')
print('处理完成！')
```

## 输出说明

- **文件**: 在原文件 `中原华北区专区数据_已更新.xlsx` 上直接修改
- **更新列**: R列（25年收益情况）、S列（26年收益情况）、T列（总收益情况）
- **标记**: 
  - 收益不为0的行：整行填充淡蓝色背景（色值：ADD8E6）
  - 收益为0的行：整行填充黄色背景（色值：FFFF00）
- **注意**: 二次匹配时，如果没有匹配成功的数据，则保持原有黄色标记

## 注意事项

1. 确保两个文件都存在且格式正确
2. 列位置固定（C列专区名称、R/S/T列收益、T/U/V列合并表收益）
3. 只处理收益都为0的行（黄色标记行）
4. 合并表中T、U、V列至少有一列不为0才参与匹配
5. 在原文件上直接修改，不创建新文件

## Skill 分组

e交易数据处理
