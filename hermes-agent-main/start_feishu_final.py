# -*- coding: utf-8 -*-
"""Hermes Feishu Gateway - FINAL VERSION"""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'
os.environ['OPENROUTER_API_KEY'] = ''
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'
os.environ['PYTHONIOENCODING'] = 'utf-8'

os.chdir(r'D:\openclaw-workspace\hermes-agent-main')

print("=" * 60)
print("Hermes Agent - Feishu Gateway")
print("=" * 60)
print("App ID: cli_a968bd97987bdcbd")
print("Model: qwen3.5-plus (AliBailian)")
print("Port: 18789")
print("=" * 60)
print()

# Patch config loading
import hermes_cli.config as hermes_config
original_load = hermes_config.load_config

def patched_load(*args, **kwargs):
    config = original_load(*args, **kwargs)
    config['providers'] = {
        'openai': {
            'enabled': True,
            'api_key': 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd',
            'base_url': 'https://coding.dashscope.aliyuncs.com/v1'
        },
        'openrouter': {'enabled': False}
    }
    config['model'] = {'default': 'qwen3.5-plus'}
    config['gateway'] = {
        'enabled': True,
        'feishu': {
            'enabled': True,
            'app_id': 'cli_a968bd97987bdcbd',
            'app_secret': 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'
        }
    }
    config['gateway_allow_all_users'] = True
    return config

hermes_config.load_config = patched_load

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
