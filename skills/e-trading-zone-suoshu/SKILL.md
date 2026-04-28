---
name: e-trading-zone-suoshu
description: e交易数据处理 - 专区所属匹配处理。根据两个Excel文件匹配专区信息，优先按专区名称匹配，匹配不上的按专区码匹配，将"所属"列数据更新到目标文件。Use when 用户需要处理e交易专区数据匹配、更新所属列、合并专区信息表。
---

# 专区所属处理 Skill

用于e交易数据处理中，将合并表中的"所属"列数据匹配更新到目标文件。

## 使用场景

- 处理中原华北区专区数据.xlsx 的"所属"列更新
- 根据专区信息汇总表_中原华北_合并.xlsx 匹配数据
- 优先按专区名称匹配，匹配不上的按专区码匹配

## 匹配规则

1. **优先匹配**: 按"专区名称"匹配
2. **备选匹配**: 名称匹配不上的，按"专区码"匹配
3. **匹配字段**:
   - 目标文件（中原华北区专区数据.xlsx）:
     - B列: 专区码
     - C列: 专区名称
     - E列: 客户类型
   - 源文件（专区信息汇总表_中原华北_合并.xlsx）:
     - B列: 专区码
     - C列: 专区名称
     - D列: 所属

## 处理流程

1. 读取两个Excel文件
2. 在目标文件的"客户类型"列（E列）右侧插入"所属"列
3. 构建匹配字典:
   - 按专区名称 → 所属
   - 按专区码 → 所属
4. 遍历目标文件，优先名称匹配，其次专区码匹配
5. 保存结果到新文件: `中原华北区专区数据_已更新.xlsx`

## Python 处理代码

```python
import pandas as pd
import os

# 文件路径
base_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件'
file1 = os.path.join(base_path, '中原华北区专区数据.xlsx')
file2 = os.path.join(base_path, '专区信息汇总表_中原华北_合并.xlsx')
output_file = os.path.join(base_path, '中原华北区专区数据_已更新.xlsx')

# 读取文件
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# 获取列名
cols1 = df1.columns.tolist()
cols2 = df2.columns.tolist()

# 关键列
zhuanqu_ma_col1 = cols1[1]      # B列: 专区码
zhuanqu_name_col1 = cols1[2]    # C列: 专区名称
kehu_type_col1 = cols1[4]       # E列: 客户类型

zhuanqu_ma_col2 = cols2[1]      # B列: 专区码
zhuanqu_name_col2 = cols2[2]    # C列: 专区名称
suoshu_col = cols2[3]           # D列: 所属

# 插入"所属"列（在客户类型列右侧，即索引5）
df1.insert(5, '所属', '')

# 构建匹配字典
name_to_suoshu = {}
ma_to_suoshu = {}

for idx, row in df2.iterrows():
    name = str(row[zhuanqu_name_col2]).strip() if pd.notna(row[zhuanqu_name_col2]) else ''
    ma = str(row[zhuanqu_ma_col2]).strip() if pd.notna(row[zhuanqu_ma_col2]) else ''
    suoshu = str(row[suoshu_col]).strip() if pd.notna(row[suoshu_col]) else ''
    
    if name and suoshu:
        name_to_suoshu[name] = suoshu
    if ma and suoshu:
        ma_to_suoshu[ma] = suoshu

# 匹配数据
for idx, row in df1.iterrows():
    name = str(row[zhuanqu_name_col1]).strip() if pd.notna(row[zhuanqu_name_col1]) else ''
    ma = str(row[zhuanqu_ma_col1]).strip() if pd.notna(row[zhuanqu_ma_col1]) else ''
    
    suoshu_value = ''
    # 优先按专区名称匹配
    if name in name_to_suoshu:
        suoshu_value = name_to_suoshu[name]
    # 名称匹配不上的，按专区码匹配
    elif ma in ma_to_suoshu:
        suoshu_value = ma_to_suoshu[ma]
    
    df1.at[idx, '所属'] = suoshu_value

# 保存结果
df1.to_excel(output_file, index=False)
print(f'处理完成，结果已保存到: {output_file}')
```

## 输出文件

- 文件名: `中原华北区专区数据_已更新.xlsx`
- 位置: 与源文件同目录
- 内容: 原数据 + 新增"所属"列

## 注意事项

1. 确保两个文件存在且格式正确
2. 列位置固定（B列专区码、C列专区名称、E列客户类型）
3. 匹配时去除前后空格
4. 未匹配到的行"所属"列为空

## Skill 分组

e交易数据处理
