import pandas as pd
import re

# 读取合并后的文件
file_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\temp\专区信息汇总表_中原华北_合并.xlsx'
df = pd.read_excel(file_path)

def parse_time_to_months(time_str):
    """将时间字符串转换为月数"""
    if pd.isna(time_str) or time_str == '' or time_str is None:
        return None
    
    time_str = str(time_str).strip()
    total_months = 0
    
    # 匹配年
    year_match = re.search(r'(\d+)年', time_str)
    if year_match:
        total_months += int(year_match.group(1)) * 12
    
    # 匹配月
    month_match = re.search(r'(\d+)月', time_str)
    if month_match:
        total_months += int(month_match.group(1))
    
    # 如果有年或月，返回总月数
    if year_match or month_match:
        return total_months
    
    return None

# 筛选条件：
# 1. 总收益为0
# 2. 上线时间距今超过3个月（如果上线时间距今为空，则取接入时间距今超过6个月）

# 转换总收益为数值
df['总收益情况'] = pd.to_numeric(df['总收益情况'], errors='coerce').fillna(0)

# 解析时间字段
df['上线时间_月数'] = df['上线时间至今'].apply(parse_time_to_months)
df['接入时间_月数'] = df['接入时间至今'].apply(parse_time_to_months)

# 条件1：总收益为0
condition_revenue = df['总收益情况'] == 0

# 条件2：时间条件
# 如果有上线时间，要求超过1年(12个月)；如果没有上线时间，要求接入时间超过1年3个月(15个月)
condition_time = (
    # 有上线时间且超过12个月
    (df['上线时间_月数'].notna() & (df['上线时间_月数'] > 12)) |
    # 没有上线时间，但有接入时间且超过15个月
    (df['上线时间_月数'].isna() & df['接入时间_月数'].notna() & (df['接入时间_月数'] > 15))
)

# 合并条件
filtered_df = df[condition_revenue & condition_time].copy()

# 选择需要的列
result = filtered_df[[' 原专区名称', '省份', '总收益情况', '专区成本', '上线时间至今', '接入时间至今', '来源Sheet']].copy()

# 按省份排序
result = result.sort_values(by=['省份', ' 原专区名称'])

print(f'筛选结果：共 {len(result)} 条记录\n')
print(result.to_string(index=False))

# 保存到Excel
output_path = r'D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\temp\专区信息汇总表_筛选结果.xlsx'
result.to_excel(output_path, index=False, sheet_name='筛选结果')
print(f'\n已保存到: {output_path}')
