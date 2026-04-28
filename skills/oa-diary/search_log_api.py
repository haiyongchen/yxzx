import os
import glob
import sys

# Windows UTF-8 支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

assets_dir = r"D:\openclaw-workspace\skills\oa-diary\oa\assets"

for md_file in glob.glob(os.path.join(assets_dir, "*.md")):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '日志' in content or 'diary' in content.lower():
                print(f"\n=== 文件：{os.path.basename(md_file)} ===")
                # 打印包含"日志"的行
                for line in content.split('\n'):
                    if '日志' in line or '日报' in line:
                        print(line[:200])
    except Exception as e:
        print(f"读取 {md_file} 失败：{e}")
