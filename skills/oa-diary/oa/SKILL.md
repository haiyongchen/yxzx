---
name: oa
description: Epoint OA 系统集成技能。通过统一的 API 封装脚本执行动作。
---

# OA 技能指导手册

你现在拥有通过统一脚本直接调用 Epoint OA 系统接口的能力。

## 1. 核心工具: `scripts/oa_api.py`

此脚本负责所有的 Token 管理、自动重试和编码处理。

**⚠️ 必须使用完整路径**，脚本位于技能目录下：
```
/Users/luyiwei/.hermes/skills/epoint/oa/scripts/oa_api.py
```

### 使用方法
```bash
python3 /Users/luyiwei/.hermes/skills/epoint/oa/scripts/oa_api.py <API_PATH> '<JSON_PARAMS>'
```

- **API_PATH**: 支持简写（如 `mail_getunreadlist_v7` 默认指向 `dynamicapi/`）或全路径。
- **JSON_PARAMS**: JSON 格式的参数字符串。

## 2. 常用操作示例

### 查看未读邮件
执行指令：
```bash
python scripts/oa_api.py mail_getunreadlist_v7 '{"currentpageindex": 0, "pagesize": 10}'
```

### 更新 OA 接口库
获取所有分类及其接口详情并存入 `assets/`：
```bash
python3 /Users/luyiwei/.hermes/skills/epoint/oa/scripts/update_api_docs.py
```

### 获取分类 (apiinnerservice)
执行指令：
```bash
python scripts/oa_api.py apiinnerservice/getApiShareCategory '{"parentGuid": "a9a648b2-9122-4404-b2b7-b60e2f4f2562"}'
```

## 3. 自动更新接口库 (每日刷新)

在执行任何 OA 相关任务之前，**必须先检查接口库是否需要更新**。判断逻辑：

1. 检查 `assets/` 目录下是否存在 `.md` 文件（即接口文档）。
2. 检查 `assets/updatetime.txt` 是否存在，并且内容是否为今天的日期（格式 `YYYY-MM-DD`）。

**如果 `assets/` 下没有 `.md` 文件，或 `updatetime.txt` 不存在，或其内容不是今天的日期**，则必须先执行：

```bash
python3 /Users/luyiwei/.hermes/skills/epoint/oa/scripts/update_api_docs.py
```

此脚本会自动拉取最新的接口清单并生成 `updatetime.txt`，确保每天只更新一次。

## 4. 动态功能发现 (自进化引擎)

当用户提出本手册未明确列出的需求时，请执行以下"动态发现"流程：

1.  **检索能力库**: 使用 `list_dir` 或 `grep_search` 查阅 `assets/` 目录下的 Markdown 文件。
    -   例如：用户想查"通讯录"，你应该去查看 `assets/通讯录.md`。
2.  **提取接口定义**: 在对应的 `.md` 文件中寻找最匹配的接口。注意查看其：
    -   `标识符` (identification)
    -   `请求参数` (结构、必填项、示例)
3.  **自主构造调用**: 使用通用工具 `scripts/oa_api.py` 发起请求。
    -   OA 邮件/通讯录/会议/任务及日志类接口：`python scripts/oa_api.py <接口标识> '<JSON_PARAMS>'`
4. **汇报结果**: 解析返回的 JSON 并根据接口描述翻译成人类可读的信息。

## 5. 执行指南

1.  **首选封装脚本**: 永远优先使用 `scripts/oa_api.py`，因为它自动处理了 Token 刷新和编码问题。
2.  **按需通过资产库查重**: 如果不确定参数，必须先 `view_file` 查阅 `assets/` 中的接口定义。
3.  **Token 失效处理**: 如果脚本提示 Token 过期且自动刷新失败，请明确告知用户并提示其扫码。
