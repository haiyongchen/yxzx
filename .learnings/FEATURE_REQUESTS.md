# Feature Requests Log

记录用户请求的功能和能力。

---

## [REQ-20260313-001] cron_notification

**Requested**: 2026-03-13T17:42:00+08:00
**Priority**: high
**Status**: pending
**Area**: cron

### Summary
所有定时任务执行完成后需要给用户发送通知

### Details
- 当前：定时任务静默执行，用户不知道是否成功
- 需求：每次任务执行完后主动通知执行结果
- 包括：成功/失败状态、执行时间、关键输出

### Affected Tasks
- git-auto-commit: Git 自动提交
- lottery-dlt-mon: 大乐透预测（周一）
- lottery-ssq-tue: 双色球预测（周二）
- lottery-dlt-wed: 大乐透预测（周三）
- lottery-ssq-thu: 双色球预测（周四）

### Suggested Implementation
1. 修改 cron 任务配置，添加通知回调
2. 或者创建一个新的监控任务
3. 使用飞书消息推送通知

### Metadata
- Source: user_request
- Tags: cron, notification, feishu
- Pattern-Key: cron.notify_on_complete

---
