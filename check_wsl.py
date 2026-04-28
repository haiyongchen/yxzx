import subprocess
import os

# 检查 wsl.exe 是否存在
wsl_exe = os.path.join(os.environ['SYSTEMROOT'], 'System32', 'wsl.exe')
exists = os.path.exists(wsl_exe)
print(f"1. WSL exe exists: {'Yes' if exists else 'No'}")

# 检查 WSL 内核
result = subprocess.run(['wsl', '--status'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
kernel_installed = result.returncode == 0
print(f"2. WSL kernel: {'Installed' if kernel_installed else 'Not installed'}")

# 检查已安装的发行版
result = subprocess.run(['wsl', '-l'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
has_distros = len(result.stdout.strip()) > 0 and 'Windows Subsystem for Linux' not in result.stdout
print(f"3. Linux distros: {'Installed' if has_distros else 'None'}")

print()
if exists and not kernel_installed:
    print("\nStatus: WSL installed but kernel missing")
    print("Run: wsl --install")
elif not exists:
    print("\nStatus: WSL not installed")
else:
    print("\nStatus: WSL ready to use")
