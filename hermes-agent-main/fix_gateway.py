# -*- coding: utf-8 -*-
"""
Fix Hermes Gateway for Windows compatibility
"""
import os
import sys

# Find the status.py file
hermes_cli_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hermes_cli')
status_file = os.path.join(hermes_cli_dir, 'status.py')

if not os.path.exists(status_file):
    print(f"File not found: {status_file}")
    sys.exit(1)

# Read the file
with open(status_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the os.kill issue for Windows
old_code = 'os.kill(pid, 0)  # signal 0 = existence check, no actual signal sent'
new_code = '''try:
        if sys.platform == 'win32':
            import subprocess
            subprocess.run(['taskkill', '/pid', str(pid), '/f', '/fi', 'status eq running'], 
                         capture_output=True, timeout=5)
            return True
        else:
            os.kill(pid, 0)
    except (OSError, subprocess.SubprocessError):
        return False'''

if old_code in content:
    content = content.replace(old_code, new_code)
    
    with open(status_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {status_file}")
else:
    print("Pattern not found, trying alternative fix...")
    # Alternative: comment out the check
    old_code2 = 'existing_pid = get_running_pid()'
    new_code2 = '# existing_pid = get_running_pid()  # Disabled for Windows compatibility'
    
    if old_code2 in content:
        content = content.replace(old_code2, new_code2)
        with open(status_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed (alternative): {status_file}")
    else:
        print("Could not find pattern to fix")
        sys.exit(1)

print("\nPlease restart the gateway")
