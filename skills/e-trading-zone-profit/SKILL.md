---
name: e-trading-zone-profit
description: e交易数据处理 - 专区收益分析处理。根据专区名称匹配三个收益文件（25年总收益、26年总收益、专区总收益），将实得收益数据更新到目标文件，无法匹配的行填充黄色背景。Use when 用户需要处理e交易专区收益数据匹配、更新收益情况、分析专区收益。
---

# 专区收益分析 Skill

用于e交易数据处理中，将三个收益文件的"实得收益"数据匹配更新到目标文件。

## 使用场景

- 处理中原华北区专区数据_已更新.xlsx 的收益列更新
- 根据25年总收益.xlsx、26年总收益.xlsx、专区总收益.xlsx 匹配数据
- 按"平台名称（财经系统）"与目标文件的"专区名称"匹配
- 无法匹配的行填充黄色背景

## 匹配规则

1. **匹配字段**:
   - 目标文件（中原华北区专区数据_已更新.xlsx）:
     - C列: 专区名称
   - 收益文件（25年总收益.xlsx、26年总收益.xlsx、专区总收益.xlsx）:
     - D列: 平台名称（财经系统）
     - I列: 实得收益

2. **匹配逻辑**:
   - 按"专区名称"与"平台名称（财经系统）"进行精确匹配
   - 去除前后空格后匹配
   - 同一平台名称的收益累加

3. **结果处理**:
   - 匹配成功: 填充对应的实得收益
   - 匹配失败: 收益为0，整行填充黄色背景

## 处理流程

1. 读取目标文件和三个收益文件
2. 在目标文件最右侧添加三列：
   - 25年收益情况
   - 26年收益情况
   - 总收益情况
3. 构建匹配字典（平台名称 → 实得收益）
4. 遍历目标文件，匹配并填充收益数据
5. 标记未匹配行为黄色背景
6. 在原文件上保存结果

## Python 处理代码

```python
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def build_match_dict(df, name_col, value_col):
    """构建匹配字典: 平台名称 -> 实得收益（累加）"""
    match_dict = {}
    for idx, row in df.iterrows():
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ''
        value = row[value_col] if pd.notna(row[value_col]) else 0
        if name:
            if name in match_dict:
                match_dict[name] += float(value) if value else 0
            else:
                match_dict[name] = float(value) if value else 0
    return match_dict

# 文件路径
base_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件'
target_file = os.path.join(base_path, '中原华北区专区数据_已更新.xlsx')

# 读取文件
df_target = pd.read_excel(target_file)
df_25 = pd.read_excel(os.path.join(base_path, '25年总收益.xlsx'))
df_26 = pd.read_excel(os.path.join(base_path, '26年总收益.xlsx'))
df_total = pd.read_excel(os.path.join(base_path, '专区总收益.xlsx'))

# 获取列名
target_cols = df_target.columns.tolist()
zhuanqu_name_col = target_cols[2]  # C列: 专区名称

profit_25_cols = df_25.columns.tolist()
profit_26_cols = df_26.columns.tolist()
profit_total_cols = df_total.columns.tolist()

# 平台名称列（D列，索引3）和实得收益列（I列，索引8）
platform_name_col_25 = profit_25_cols[3]
shide_shouyi_col_25 = profit_25_cols[8]
platform_name_col_26 = profit_26_cols[3]
shide_shouyi_col_26 = profit_26_cols[8]
platform_name_col_total = profit_total_cols[3]
shide_shouyi_col_total = profit_total_cols[8]

# 构建匹配字典
dict_25 = build_match_dict(df_25, platform_name_col_25, shide_shouyi_col_25)
dict_26 = build_match_dict(df_26, platform_name_col_26, shide_shouyi_col_26)
dict_total = build_match_dict(df_total, platform_name_col_total, shide_shouyi_col_total)

# 添加三列到目标文件
df_target['25年收益情况'] = 0.0
df_target['26年收益情况'] = 0.0
df_target['总收益情况'] = 0.0

# 匹配数据并记录未匹配行
unmatched_rows = []

for idx, row in df_target.iterrows():
    name = str(row[zhuanqu_name_col]).strip() if pd.notna(row[zhuanqu_name_col]) else ''
    
    val_25 = dict_25.get(name, 0)
    val_26 = dict_26.get(name, 0)
    val_total = dict_total.get(name, 0)
    
    df_target.at[idx, '25年收益情况'] = val_25
    df_target.at[idx, '26年收益情况'] = val_26
    df_target.at[idx, '总收益情况'] = val_total
    
    # 如果三个都没有匹配上，记录行号
    if val_25 == 0 and val_26 == 0 and val_total == 0:
        unmatched_rows.append(idx)

# 保存数据
df_target.to_excel(target_file, index=False)

# 使用openpyxl填充黄色背景
wb = load_workbook(target_file)
ws = wb.active

# 黄色填充
yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

# 对未匹配的行填充黄色
for row_idx in unmatched_rows:
    excel_row = row_idx + 2  # DataFrame索引从0开始，Excel从1开始，还要算上表头
    for col in range(1, ws.max_column + 1):
        ws.cell(row=excel_row, column=col).fill = yellow_fill

wb.save(target_file)
print(f'处理完成！未匹配行数: {len(unmatched_rows)}，已填充黄色背景')
```

## 输出说明

- **文件**: 在原文件 `中原华北区专区数据_已更新.xlsx` 上直接修改
- **新增列**: 
  - 25年收益情况
  - 26年收益情况
  - 总收益情况
- **标记**: 完全未匹配的行（三列收益都为0）整行填充黄色背景

## 注意事项

1. 确保四个文件都存在且格式正确
2. 列位置固定（D列平台名称、I列实得收益）
3. 匹配时去除前后空格
4. 同一平台名称的收益会累加
5. 在原文件上直接修改，不创建新文件

## Skill 分组

e交易数据处理
