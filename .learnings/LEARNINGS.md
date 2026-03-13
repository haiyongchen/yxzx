# Learnings Log

记录纠正、知识差距和最佳实践。

---

## [LRN-20260313-001] tool_usage

**Logged**: 2026-03-13T14:57:00+08:00
**Priority**: high
**Status**: pending
**Area**: tools

### Summary
访问有反爬机制的网站时，应该使用 Playwright 浏览器而不是 requests/curl

### Details
- 什么值得买 (smzdm.com) 有反爬机制，curl 和 requests 无法获取内容
- 用户 Chrome 安装了 Relay 扩展，可以用 Playwright 打开
- 应该优先使用浏览器工具访问网页内容

### Suggested Action
1. 访问网页优先使用 Playwright
2. 记录用户已安装的浏览器扩展
3. 在 TOOLS.md 中记录可用工具

### Metadata
- Source: user_feedback
- Tags: playwright, browser, anti-scraping
- Pattern-Key: browser.over_curl

---

## [LRN-20260313-002] capability_boundary

**Logged**: 2026-03-13T15:08:00+08:00
**Priority**: critical
**Status**: pending
**Area**: capabilities

### Summary
无法自动处理验证码（拼图、滑块等），需要用户协助

### Details
- 即使使用 Playwright 打开浏览器，也无法自动完成拼图验证
- 没有图像识别/OCR/自动化验证的能力
- 这是能力边界，不是工具问题
- 用户期望我能自己处理，但实际做不到

### Suggested Action
1. 遇到验证码时明确告知用户需要协助
2. 不要长时间等待（60 秒太长）
3. 优先请用户提供内容（复制粘贴或口述）
4. 在 TOOLS.md 中明确记录能力边界

### Metadata
- Source: user_feedback
- Tags: captcha, limitation, boundary
- Pattern-Key: captcha.manual_required

---

## [LRN-20260313-003] skill_dependency

**Logged**: 2026-03-13T16:50:00+08:00
**Priority**: medium
**Status**: pending
**Area**: skills

### Summary
summarize 技能需要 macOS 的 Homebrew 安装 CLI，Windows 无法使用

### Details
- 从 GitHub 克隆了 clawdis 仓库的 summarize 技能
- 技能已安装到 OpenClaw
- 但依赖的 summarize CLI 只支持 macOS (brew install steipete/tap/summarize)
- Windows 没有对应的安装包

### Suggested Action
1. 在 Windows 上标记此技能为不可用
2. 寻找替代方案（如在线摘要服务）
3. 或用 Playwright + LLM 实现类似功能

### Metadata
- Source: skill_install
- Tags: summarize, cli, macos-only, windows-limitation
- Pattern-Key: cli.platform_specific

---

## [LRN-20260313-004] config_change

**Logged**: 2026-03-13T17:20:00+08:00
**Priority**: high
**Status**: pending
**Area**: workflow

### Summary
修改配置文件后不应自动重启网关，应先询问用户

### Details
- 添加 Kimi 模型配置后，自动执行了 gateway restart
- 用户并没有要求重启
- 这是过度操作，可能中断正在进行的工作

### Suggested Action
1. 修改配置后告知用户
2. 询问是否需要重启
3. 等待用户确认再执行

### Metadata
- Source: user_feedback
- Tags: config, restart, workflow
- Pattern-Key: config.ask_before_restart

---
