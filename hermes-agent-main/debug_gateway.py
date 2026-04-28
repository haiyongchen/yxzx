# -*- coding: utf-8 -*-
"""Debug gateway startup"""
import os
import yaml

os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

# Load config
config_path = os.path.expanduser("~/.hermes/config.yaml")
config = yaml.safe_load(open(config_path, 'r', encoding='utf-8'))

print("Config loaded:")
print(f"  Gateway enabled: {config.get('gateway', {}).get('enabled')}")
print(f"  Feishu enabled: {config.get('gateway', {}).get('feishu', {}).get('enabled')}")
print(f"  Feishu app_id: {config.get('gateway', {}).get('feishu', {}).get('app_id')}")
print()

# Check what Hermes sees
from hermes_cli import config as hconfig
loaded = hconfig.load_config()
print("Hermes loaded config:")
print(f"  Gateway: {loaded.get('gateway')}")
print(f"  Feishu: {loaded.get('gateway', {}).get('feishu')}")
