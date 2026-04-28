# -*- coding: utf-8 -*-
from docx import Document
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

doc = Document(r'C:\Users\63111\Desktop\接口文档-admin-20260420.docx')

print("=" * 60)
print("接口文档内容分析")
print("=" * 60)

# 查找所有表格
for i, table in enumerate(doc.tables):
    print(f"\n=== 表格 {i+1} ===")
    for j, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
        if cells:
            print(f"  行{j+1}: {' | '.join(cells[:5])}")

# 查找包含接口名称的段落
print("\n\n=== 接口列表 ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    # 查找接口名称模式
    if text and ('接口' in text or 'API' in text):
        # 跳过纯术语定义
        if not any(x in text for x in ['术语', '定义', 'RFC', 'HTTP', 'JSON', 'XML', 'REST']):
            print(f'[{i}] {text[:200]}')
