# -*- coding: utf-8 -*-
"""
Hermes Gateway Launcher with UTF-8 encoding fix
"""
import os
import sys
import io

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Set environment
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Change to Hermes directory
os.chdir(r'D:\openclaw-workspace\hermes-agent-main')

print("=" * 60)
print("Hermes Agent - Feishu Gateway")
print("=" * 60)
print(f"App ID: cli_a968bd97987bdcbd")
print(f"Model: qwen3.5-plus (Bailian)")
print(f"Port: 18789")
print("=" * 60)
print()

# Import and run
from hermes_cli.main import main
sys.argv = ['hermes', 'gateway', 'run']

try:
    main()
except KeyboardInterrupt:
    print("\n\nStopped by user")
except Exception as e:
    print(f"\n\nERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
