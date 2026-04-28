# -*- coding: utf-8 -*-
"""Force Bailian configuration"""
import os
import json
import yaml

hermes_home = os.path.expanduser("~/.hermes")

# Fix config.yaml
config = {
    "model": {"default": "qwen3.5-plus"},
    "providers": {
        "openai": {
            "enabled": True,
            "api_key": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1"
        }
    },
    "gateway": {
        "enabled": True,
        "feishu": {
            "enabled": True,
            "app_id": "cli_a968bd97987bdcbd",
            "app_secret": "Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0"
        }
    },
    "gateway_allow_all_users": True
}

with open(os.path.join(hermes_home, "config.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)
print("Fixed config.yaml")

# Fix auth.json
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
            "id": "bailian-01",
            "label": "AliBailian",
            "auth_type": "api_key",
            "priority": 1,
            "access_token": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1",
            "enabled": True
        }]
    }
}

with open(os.path.join(hermes_home, "auth.json"), "w", encoding="utf-8") as f:
    json.dump(auth, f, indent=2, ensure_ascii=False)
print("Fixed auth.json")

print("\nDone! Restart the gateway.")
