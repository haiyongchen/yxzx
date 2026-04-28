---
name: e-trading-zone-cost-first
description: e交易数据处理 - 专区成本初次匹配。根据合同编号匹配合同人工成本统计表，将实际人工成本数据更新到目标文件，未匹配的行填充黄色背景。Use when 用户需要处理e交易专区成本数据匹配、更新实际人工成本、初次成本匹配。
---

# 专区成本初次匹配 Skill

用于e交易数据处理中，根据合同编号匹配并更新实际人工成本数据。

## 使用场景

- 处理中原华北区专区数据_已更新.xlsx 的实际人工成本列
- 根据合同人工成本统计.xlsx 匹配数据
- 按"合同编号"进行匹配
- 未匹配的行填充黄色背景

## 匹配规则

1. **匹配字段**:
   - 目标文件（中原华北区专区数据_已更新.xlsx）:
     - A列: 合同编号 (Unnamed: 0)
   - 成本文件（合同人工成本统计.xlsx）:
     - B列: 合同编号
     - C列: 实际人工成本

2. **匹配逻辑**:
   - 按"合同编号"进行精确匹配
   - 去除前后空格后匹配
   - 同一合同编号的成本累加

3. **结果处理**:
   - 匹配成功: 填充对应的实际人工成本
   - 匹配失败: 成本为0，整行填充黄色背景

## 处理流程

1. 读取目标文件和成本文件
2. 在目标文件最右侧添加"实际人工成本"列
3. 构建匹配字典（合同编号 → 实际人工成本，累加）
4. 遍历目标文件，匹配并填充成本数据
5. 标记未匹配行为黄色背景
6. 保存到新文件

## Python 处理代码

```python
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# 文件路径
base_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件'
target_file = os.path.join(base_path, '中原华北区专区数据_已更新.xlsx')
cost_file = os.path.join(base_path, '合同人工成本统计.xlsx')

# 读取文件
df_target = pd.read_excel(target_file)
df_cost = pd.read_excel(cost_file)

# 获取列名
target_cols = df_target.columns.tolist()
cost_cols = df_cost.columns.tolist()

# 关键列
hetong_no_col_target = target_cols[0]    # A列: 合同编号 (Unnamed: 0)
hetong_no_col_cost = cost_cols[1]        # B列: 合同编号
cost_col = cost_cols[2]                  # C列: 实际人工成本

# 构建成本匹配字典（同一合同编号累加）
cost_dict = {}
for idx, row in df_cost.iterrows():
    hetong_no = str(row[hetong_no_col_cost]).strip() if pd.notna(row[hetong_no_col_cost]) else ''
    cost_val = row[cost_col] if pd.notna(row[cost_col]) else 0
    if hetong_no:
        try:
            cost_float = float(cost_val) if cost_val else 0
            if hetong_no in cost_dict:
                cost_dict[hetong_no] += cost_float
            else:
                cost_dict[hetong_no] = cost_float
        except:
            if hetong_no not in cost_dict:
                cost_dict[hetong_no] = 0

# 在目标文件最右侧添加"实际人工成本"列
df_target['实际人工成本'] = 0.0

# 匹配数据
matched_count = 0
unmatched_rows = []

for idx, row in df_target.iterrows():
    hetong_no = str(row[hetong_no_col_target]).strip() if pd.notna(row[hetong_no_col_target]) else ''
    
    if hetong_no in cost_dict:
        df_target.at[idx, '实际人工成本'] = cost_dict[hetong_no]
        matched_count += 1
    else:
        unmatched_rows.append(idx)

print(f'匹配成功: {matched_count} 条')
print(f'未匹配: {len(unmatched_rows)} 条')

# 保存到新文件
output_file = os.path.join(base_path, '中原华北区专区数据_成本更新.xlsx')
df_target.to_excel(output_file, index=False)
print(f'数据已保存到: {output_file}')

# 使用openpyxl填充颜色（未匹配的行填充黄色）
wb = load_workbook(output_file)
ws = wb.active

# 定义颜色
yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

# 对未匹配的行填充黄色
for row_idx in unmatched_rows:
    excel_row = row_idx + 2  # DataFrame索引从0开始，Excel从1开始，还要算上表头
    for col in range(1, ws.max_column + 1):
        ws.cell(row=excel_row, column=col).fill = yellow_fill

wb.save(output_file)
print(f'黄色背景已填充到 {len(unmatched_rows)} 行')
print('处理完成！')
```

## 输出说明

- **文件**: `中原华北区专区数据_成本更新.xlsx`
- **新增列**: 实际人工成本
- **标记**: 未匹配的行整行填充黄色背景

## 注意事项

1. 确保两个文件都存在且格式正确
2. 列位置固定（A列合同编号、B列成本文件合同编号、C列实际人工成本）
3. 匹配时去除前后空格
4. 同一合同编号的成本会累加
5. 保存到新文件，不覆盖原文件

## Skill 分组

e交易数据处理
