import os
import subprocess
import sys

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'D:\work\运营中心\yxzx\阳光优采\需求\在线支付'

# Find the docx and xlsx files
for f in os.listdir(base_dir):
    if f.endswith('.docx'):
        docx_path = os.path.join(base_dir, f)
        print(f"DOCX: {docx_path}")
    elif f.endswith('.xlsx'):
        xlsx_path = os.path.join(base_dir, f)
        print(f"XLSX: {xlsx_path}")

# Convert docx to markdown using pandoc
print("\n=== Converting DOCX to Markdown ===")
md_output = os.path.join(os.environ['TEMP'], 'sunshine_doc.md')
result = subprocess.run(['pandoc', docx_path, '-o', md_output, '--wrap=none'], 
                       capture_output=True, text=True, encoding='utf-8')
if result.returncode == 0:
    print(f"Converted to: {md_output}")
    with open(md_output, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content[:20000])
else:
    print(f"Error: {result.stderr}")
