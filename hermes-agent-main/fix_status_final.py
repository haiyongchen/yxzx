# -*- coding: utf-8 -*-
"""Final fix for status.py Windows compatibility"""

filepath = 'D:/openclaw-workspace/hermes-agent-main/gateway/status.py'
content = open(filepath, 'r', encoding='utf-8').read()

# Add Windows-safe kill function after imports
import_section_end = content.find('\ndef ')
if import_section_end == -1:
    import_section_end = content.find('\n\nclass ')

if import_section_end > 0:
    wrapper = '''

def _safe_kill(pid, sig):
    """Windows-compatible process signal"""
    import platform
    import subprocess
    if platform.system() == 'Windows':
        try:
            subprocess.run(['taskkill', '/pid', str(pid), '/f'], capture_output=True, timeout=5)
        except Exception:
            pass
    else:
        import signal
        os.kill(pid, sig)

'''
    content = content[:import_section_end] + wrapper + content[import_section_end:]
    
    # Replace all os.kill calls
    content = content.replace('os.kill(pid, 0)', '_safe_kill(pid, 0)')
    content = content.replace('os.kill(existing_pid, 0)', '_safe_kill(existing_pid, 0)')
    
    open(filepath, 'w', encoding='utf-8').write(content)
    print(f"Fixed: {filepath}")
else:
    print("Could not find import section")
