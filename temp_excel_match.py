import pandas as pd
import os

# 文件路径
file1_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\同步数据文件\专区接入情况统计表_已整合_修正版.xlsx'
file2_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件\综合成果数据\中原华北区saas专区总数据.xlsx'

print("=" * 60)
print("开始处理Excel数据匹配任务")
print("=" * 60)

# 读取两个文件
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# 获取列名
cols1 = df1.columns.tolist()
cols2 = df2.columns.tolist()

print(f"\n文件1: 专区接入情况统计表_已整合_修正版.xlsx")
print(f"  总行数: {len(df1)}")
print(f"  B列(专区码): {cols1[1]}")
print(f"  C列(专区名称): {cols1[2]}")
print(f"  S列(专区地址): {cols1[18]}")

print(f"\n文件2: 中原华北区saas专区总数据.xlsx")
print(f"  总行数: {len(df2)}")
print(f"  B列(专区码): {cols2[1]}")
print(f"  C列(专区名称): {cols2[2]}")

# 创建匹配键（处理空值）
def create_match_key(row, code_col, name_col):
    code = str(row[code_col]) if pd.notna(row[code_col]) else ''
    name = str(row[name_col]) if pd.notna(row[name_col]) else ''
    return f"{code.strip()}|{name.strip()}"

# 为文件1创建匹配字典
print("\n正在创建匹配字典...")
match_dict = {}
for idx, row in df1.iterrows():
    key = create_match_key(row, cols1[1], cols1[2])
    if key and key != '|':  # 排除空键
        match_dict[key] = row[cols1[18]]  # 专区地址

print(f"  文件1有效匹配键数量: {len(match_dict)}")

# 为文件2添加专区地址列
print("\n正在匹配数据...")
df2['专区地址'] = ''

matched_count = 0
unmatched_count = 0
empty_key_count = 0

for idx, row in df2.iterrows():
    key = create_match_key(row, cols2[1], cols2[2])
    
    if key == '|':
        empty_key_count += 1
        continue
    
    if key in match_dict:
        df2.at[idx, '专区地址'] = match_dict[key]
        matched_count += 1
    else:
        unmatched_count += 1

print(f"\n匹配结果统计:")
print(f"  成功匹配: {matched_count} 行")
print(f"  未匹配: {unmatched_count} 行")
print(f"  空键(专区码和名称都为空): {empty_key_count} 行")

# 保存结果
print("\n正在保存文件...")
df2.to_excel(file2_path, index=False)
print(f"  文件已保存: {file2_path}")

# 显示部分匹配结果
print("\n前5行匹配结果预览:")
preview_cols = [cols2[1], cols2[2], '专区地址']
print(df2[preview_cols].head())

print("\n" + "=" * 60)
print("任务完成!")
print("=" * 60)
