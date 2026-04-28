# -*- coding: utf-8 -*-
"""Force start Feishu gateway with Bailian"""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Hardcode credentials
API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'

os.environ['OPENAI_API_KEY'] = API_KEY
os.environ['OPENAI_BASE_URL'] = BASE_URL
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'
os.environ['PYTHONIOENCODING'] = 'utf-8'

os.chdir(r'D:\openclaw-workspace\hermes-agent-main')

print("=" * 60)
print("Hermes Agent - Feishu Gateway")
print("=" * 60)
print(f"App ID: {FEISHU_APP_ID}")
print(f"Model: qwen3.5-plus (Bailian)")
print(f"Port: 18789")
print("=" * 60)
print()

# Patch Hermes config BEFORE any gateway code runs
import hermes_cli.config as hconfig

original_get = hconfig.get_config

def forced_get_config():
    return {
        'model': {'default': 'qwen3.5-plus'},
        'providers': {
            'openai': {
                'enabled': True,
                'api_key': API_KEY,
                'base_url': BASE_URL,
                'models': ['qwen3.5-plus']
            },
            'openrouter': {'enabled': False}
        },
        'gateway': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': 18789,
            'feishu': {
                'enabled': True,
                'app_id': FEISHU_APP_ID,
                'app_secret': FEISHU_APP_SECRET
            }
        },
        'gateway_allow_all_users': True,
        'agent': {'name': 'Hermes', 'temperature': 0.7}
    }

hconfig.get_config = forced_get_config

from hermes_cli.main import main
sys.argv = ['hermes', 'gateway', 'run']

try:
    main()
except KeyboardInterrupt:
    print("\n\nStopped")
except Exception as e:
    print(f"\n\nERROR: {e}")
    import traceback
    traceback.print_exc()
