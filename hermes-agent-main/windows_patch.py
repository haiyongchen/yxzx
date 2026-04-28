# -*- coding: utf-8 -*-
"""Windows compatibility patch for Hermes Gateway"""
import os

files_to_patch = [
    'D:/openclaw-workspace/hermes-agent-main/gateway/status.py',
    'D:/openclaw-workspace/hermes-agent-main/gateway/platforms/feishu.py',
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        print(f"Skip: {filepath} (not found)")
        continue
    
    content = open(filepath, 'r', encoding='utf-8').read()
    original = content
    
    # Add Windows-safe os.kill wrapper at the top
    wrapper_code = '''
import platform
def _safe_kill(pid, sig):
    """Windows-compatible process signal"""
    if platform.system() == 'Windows':
        import subprocess
        try:
            subprocess.run(['taskkill', '/pid', str(pid), '/f'], capture_output=True, timeout=5)
        except:
            pass
    else:
        import signal
        os.kill(pid, sig)

'''
    
    # Replace os.kill calls
    content = content.replace('os.kill(pid, 0)', '_safe_kill(pid, 0)')
    content = content.replace('os.kill(existing_pid, 0)', '_safe_kill(existing_pid, 0)')
    content = content.replace('os.kill(pid, sig)', '_safe_kill(pid, sig)')
    content = content.replace('os.kill(pid, signal.SIGTERM)', '_safe_kill(pid, signal.SIGTERM)')
    content = content.replace('os.kill(..., SIGTERM)', '_safe_kill(..., SIGTERM)')
    
    # Add wrapper at the top after imports
    if '_safe_kill' not in content and 'import platform' not in content.split('\n')[20]:
        # Find a good place to insert (after imports)
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines[:50]):
            if line.startswith('import ') or line.startswith('from '):
                insert_pos = i + 1
        
        if insert_pos > 0:
            lines.insert(insert_pos, wrapper_code)
            content = '\n'.join(lines)
            print(f"Patched: {filepath}")
        else:
            print(f"Skip: {filepath} (couldn't find insert position)")
            content = original
    
    if content != original:
        open(filepath, 'w', encoding='utf-8').write(content)
        print(f"Fixed: {filepath}")

print("\nDone! Restart gateway.")
