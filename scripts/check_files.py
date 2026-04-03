# -*- coding: utf-8 -*-
from pathlib import Path

revenue_dir = Path('D:/work/运营中心/yxzx/新点e交易相关材料/日常数据运维工具/同步数据文件/e交易收益情况')
for f in revenue_dir.glob('*.xlsx'):
    if not f.name.startswith('~'):
        print(f'文件名: {f.name}')
