# -*- coding: utf-8 -*-
"""Force Bailian configuration for Hermes"""
import os
import json
import yaml

hermes_home = os.path.expanduser("~/.hermes")

# 1. Fix config.yaml
config = {
    "model": {"default": "qwen3.5-plus"},
    "providers": {
        "openai": {
            "enabled": True,
            "api_key": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1",
            "models": ["qwen3.5-plus", "qwen-turbo", "qwen-max"]
        },
        "openrouter": {"enabled": False}
    },
    "gateway": {
        "enabled": True,
        "host": "0.0.0.0",
        "port": 18789,
        "feishu": {
            "enabled": True,
            "app_id": "cli_a968bd97987bdcbd",
            "app_secret": "Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0"
        }
    },
    "gateway_allow_all_users": True,
    "agent": {"name": "Hermes", "temperature": 0.7}
}

config_path = os.path.join(hermes_home, "config.yaml")
with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
print("Fixed: " + config_path)

# 2. Fix auth.json
auth = {
    "version": 1,
    "providers": {
        "openai": {
            "api_key": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1",
            "enabled": True
        }
    },
    "credential_pool": {
        "openai": [{
            "id": "bailian-primary",
            "label": "AliBailian",
            "auth_type": "api_key",
            "priority": 1,
            "access_token": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1",
            "enabled": True,
            "exhausted": False
        }],
        "openrouter": []
    }
}

auth_path = os.path.join(hermes_home, "auth.json")
with open(auth_path, "w", encoding="utf-8") as f:
    json.dump(auth, f, indent=2, ensure_ascii=False)
print("Fixed: " + auth_path)

# 3. Fix .env
env_content = "OPENAI_API_KEY=sk-sp-896d84d6b8d946cea3d7e45d48c196dd\nOPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1\nOPENROUTER_API_KEY=\nGATEWAY_ALLOW_ALL_USERS=true\n"
env_path = os.path.join(hermes_home, ".env")
with open(env_path, "w", encoding="utf-8") as f:
    f.write(env_content)
print("Fixed: " + env_path)

print("\nALL CONFIGURATION FIXED!")
print("Restart gateway: python D:\\openclaw-workspace\\hermes-agent-main\\force_start.py")
