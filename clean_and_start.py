# -*- coding: utf-8 -*-
"""Clean locks and start Hermes gateway"""
import sqlite3
import os
import shutil
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("  Cleaning locks and starting Hermes Gateway")
print("=" * 60)

# 1. Clean database locks
db_path = r'C:\Users\63111\.hermes\state.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('DELETE FROM scoped_locks')
        print(f"Deleted {c.rowcount} locks from database")
    except Exception as e:
        print(f"No locks table: {e}")
    conn.commit()
    conn.close()

# 2. Clean locks directory
locks_dir = r'C:\Users\63111\.hermes\locks'
shutil.rmtree(locks_dir, ignore_errors=True)
print("Cleared locks directory")

# 3. Clean PID files
hermes_home = r'C:\Users\63111\.hermes'
for f in os.listdir(hermes_home):
    if '.pid' in f or 'lock' in f:
        os.remove(os.path.join(hermes_home, f))
        print(f"Removed {f}")

print("\nCleanup complete! Starting gateway...\n")
print("=" * 60)

# 4. Set environment and start
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'
os.environ['PYTHONIOENCODING'] = 'utf-8'

os.chdir(r'D:\openclaw-workspace\hermes-agent-main')

from hermes_cli.main import main
sys.argv = ['hermes', 'gateway', 'run']

try:
    main()
except KeyboardInterrupt:
    print("\n\nStopped by user")
except Exception as e:
    print(f"\n\nERROR: {e}")
