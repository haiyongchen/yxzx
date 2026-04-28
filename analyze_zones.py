import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取Excel文件
file_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\e交易数据分析处理文件\中原华北区专区数据_成本更新.xlsx'
df = pd.read_excel(file_path, sheet_name='大企业专区')

# 转换收益列为数值型
df['25年收益情况'] = pd.to_numeric(df['25年收益情况'], errors='coerce').fillna(0)
df['26年收益情况'] = pd.to_numeric(df['26年收益情况'], errors='coerce').fillna(0)
df['总收益情况'] = pd.to_numeric(df['总收益情况'], errors='coerce').fillna(0)

# 解析'上线至今'列
def parse_time(text):
    if pd.isna(text):
        return 0, 0
    text = str(text)
    import re
    years = 0
    months = 0
    
    year_match = re.search(r'(\d+)年', text)
    if year_match:
        years = int(year_match.group(1))
    
    month_match = re.search(r'(\d+)月', text)
    if month_match:
        months = int(month_match.group(1))
    
    return years, months

# 应用解析
time_data = df['上线至今'].apply(parse_time)
df['上线年数'] = [x[0] for x in time_data]
df['上线月数'] = [x[1] for x in time_data]

print('=== 中原华北区大企业专区 - 八大指标完整分析 ===\n')
print('总专区数:', len(df))
print()

# 指标一：接入超过1年，总收益为0
指标一 = df[(df['上线年数'] >= 1) & (df['总收益情况'] == 0)]
print('【指标一】接入超过1年，总收益为0:', len(指标一), '个')
for idx, row in 指标一.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 上线', row['上线至今'])
print()

# 指标二：接入超过1年，0<总收益<10w
指标二 = df[(df['上线年数'] >= 1) & (df['总收益情况'] > 0) & (df['总收益情况'] < 100000)]
print('【指标二】接入超过1年，0<总收益<10万:', len(指标二), '个')
for idx, row in 指标二.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 总收益:', int(row['总收益情况']))
print()

# 指标三：接入超过1年，0<总收益<5w
指标三 = df[(df['上线年数'] >= 1) & (df['总收益情况'] > 0) & (df['总收益情况'] < 50000)]
print('【指标三】接入超过1年，0<总收益<5万:', len(指标三), '个')
for idx, row in 指标三.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 总收益:', int(row['总收益情况']))
print()

# 指标四：接入超过3个月，小于1年，总收益为0
指标四 = df[(df['上线年数'] == 0) & (df['上线月数'] >= 3) & (df['总收益情况'] == 0)]
print('【指标四】接入超过3个月小于1年，总收益为0:', len(指标四), '个')
for idx, row in 指标四.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 上线', row['上线至今'])
print()

# 指标五：25年前接入，0<25年收益<10w
指标五 = df[(df['上线年数'] >= 1) & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 100000)]
print('【指标五】25年前接入，0<25年收益<10万:', len(指标五), '个')
for idx, row in 指标五.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 25年收益:', int(row['25年收益情况']))
print()

# 指标六：25年前接入，0<25年收益<5w
指标六 = df[(df['上线年数'] >= 1) & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 50000)]
print('【指标六】25年前接入，0<25年收益<5万:', len(指标六), '个')
for idx, row in 指标六.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 25年收益:', int(row['25年收益情况']))
print()

# 指标七：26年产生收益
指标七 = df[df['26年收益情况'] > 0]
print('【指标七】26年产生收益:', len(指标七), '个')
for idx, row in 指标七.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 26年收益:', int(row['26年收益情况']))
print()

# 指标八：25年有收益，26年无
指标八 = df[(df['25年收益情况'] > 0) & (df['26年收益情况'] == 0)]
print('【指标八】25年有收益，26年无收益:', len(指标八), '个')
for idx, row in 指标八.iterrows():
    print('  -', row['专区名称'], '(' + row['分公司'] + ') - 25年:', int(row['25年收益情况']), ', 26年:0')
print()

# 汇总统计
print('=' * 60)
print('【汇总统计】')
print('  总专区数:', len(df), '个')
print('  长期零收益(>1年):', len(指标一), '个')
print('  长期微收益(>1年,<5万):', len(指标三), '个')
print('  26年活跃专区:', len(指标七), '个 (', round(len(指标七)/len(df)*100, 1), '%)')
print('  26年断流专区:', len(指标八), '个')
