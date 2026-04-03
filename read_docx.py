# -*- coding: utf-8 -*-
from docx import Document
import os

doc_path = 'D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\e交易专区收益成本统计报告.docx'

# 读取Word文档
doc = Document(doc_path)

print("=" * 80)
print("e交易专区收益成本统计报告 - 内容分析")
print("=" * 80)

# 提取所有段落
print("\n【文档段落内容】\n")
for i, para in enumerate(doc.paragraphs):
    if para.text.strip():
        print(f"段落 {i+1}: {para.text}")

# 提取所有表格
print("\n\n【文档表格内容】\n")
for table_idx, table in enumerate(doc.tables):
    print(f"\n--- 表格 {table_idx + 1} ---")
    for row_idx, row in enumerate(table.rows):
        row_data = [cell.text for cell in row.cells]
        print(f"行 {row_idx + 1}: {row_data}")

# 检查是否有嵌入式Excel
print("\n\n【嵌入式对象】\n")
# Word文档中的嵌入对象通常在word/embeddings目录下
embeddings_path = os.path.join(os.path.dirname(doc_path), 'temp_embeddings')
print(f"文档包含嵌入式对象，需要进一步分析")

print("\n" + "=" * 80)
