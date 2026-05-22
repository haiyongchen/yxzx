import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 电商名单
ecommerce_list = [
    '苏宁易购集团股份有限公司',
    '得力集团有限公司',
    '欧菲斯集团股份有限公司',
    '深圳齐心集团股份有限公司',
    '大江科技集团有限公司',
    '史泰博(上海)有限公司',
    '阳采集团有限公司',
    '江苏比高机电设备有限公司',
    '浙江宏伟供应链集团股份有限公司',
    '深圳市怡亚通供应链股份有限公司',
    '咸亨国际科技股份有限公司',
    '紫迈电子商务有限公司',
    '鑫方盛数智科技股份有限公司',
    '震坤行工业超市（上海）有限公司'
]

# 读取文件
file_path = r'D:\work\龙虾可操作需求临时文件夹\订单数据处理\阳光优采交易订单.xlsx'
df = pd.read_excel(file_path)

print('=== 处理前J列分布 ===')
print(df['供应商类型'].value_counts())
print()

# 定义判断函数
def check_supplier_type(name):
    if pd.isna(name):
        return '本地供应商'
    name = str(name).strip()
    # 精确匹配
    if name in ecommerce_list:
        return '电商供应商'
    # 处理"史泰博"这种简称
    for ecom in ecommerce_list:
        if '史泰博' in name and '史泰博' in ecom:
            return '电商供应商'
    return '本地供应商'

# 重新判断供应商类型
df['供应商类型_new'] = df['供应商'].apply(check_supplier_type)

print('=== 处理后J列分布 ===')
print(df['供应商类型_new'].value_counts())
print()

# 对比新旧差异
diff = df[df['供应商类型'] != df['供应商类型_new']]
print(f'=== 有变化的行数: {len(diff)} ===')
if len(diff) > 0:
    print('变化明细:')
    for _, row in diff.iterrows():
        print(f'  供应商: {row["供应商"]} | 原类型: {row["供应商类型"]} -> 新类型: {row["供应商类型_new"]}')
print()

# 更新J列
df['供应商类型'] = df['供应商类型_new']
df = df.drop(columns=['供应商类型_new'])

# 保存文件
output_path = r'D:\work\龙虾可操作需求临时文件夹\订单数据处理\阳光优采交易订单_处理后.xlsx'
df.to_excel(output_path, index=False)
print(f'文件已保存到: {output_path}')
