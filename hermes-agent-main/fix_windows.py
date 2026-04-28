# -*- coding: utf-8 -*-
"""Fix Windows compatibility for Hermes Gateway"""
import os

# Fix status.py
status_file = 'D:/openclaw-workspace/hermes-agent-main/gateway/status.py'
content = open(status_file, 'r', encoding='utf-8').read()

# Replace the os.kill call with Windows-compatible code
old_code = '''    try:
        os.kill(pid, 0)  # signal 0 = existence check, no actual signal sent
    except (ProcessLookupError, PermissionError):
        remove_pid_file()
        return None'''

new_code = '''    try:
        if os.name == 'nt':  # Windows
            import subprocess
            result = subprocess.run(['taskkill', '/pid', str(pid), '/f', '/fi', 'status eq running'], 
                                   capture_output=True, timeout=5)
            if result.returncode != 0:
                remove_pid_file()
                return None
        else:
            os.kill(pid, 0)
    except (ProcessLookupError, PermissionError, OSError, subprocess.SubprocessError):
        remove_pid_file()
        return None'''

if old_code in content:
    content = content.replace(old_code, new_code)
    open(status_file, 'w', encoding='utf-8').write(content)
    print(f"Fixed: {status_file}")
else:
    print("Pattern not found in status.py")
    print("Searching for os.kill...")
    if 'os.kill' in content:
        print("Found os.kill but pattern doesn't match exactly")
        # Show context
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'os.kill' in line:
                print(f"Line {i}: {line}")
