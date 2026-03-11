# Git 自动推送脚本

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `auto-push.ps1` | 自动推送脚本（定时任务调用） |
| `test-push.ps1` | 测试推送脚本（手动测试用） |
| `push-log.txt` | 推送日志（自动创建） |

## ⏰ 定时任务配置

- **任务名称**: `YXZX-Git-AutoPush`
- **执行时间**: 每天晚上 23:00
- **执行内容**: 自动添加、提交并推送所有更改到 GitHub

## 🚀 手动测试

如需手动测试推送功能，运行：
```powershell
D:\work\运营中心\yxzx\scripts\test-push.ps1
```

## 📋 查看日志

推送日志保存在：
```
D:\work\运营中心\yxzx\scripts\push-log.txt
```

## 🔧 管理定时任务

### 查看任务状态
```powershell
Get-ScheduledTask -TaskName "YXZX-Git-AutoPush" | Get-ScheduledTaskInfo
```

### 手动触发任务
```powershell
Start-ScheduledTask -TaskName "YXZX-Git-AutoPush"
```

### 暂停任务
```powershell
Disable-ScheduledTask -TaskName "YXZX-Git-AutoPush"
```

### 启用任务
```powershell
Enable-ScheduledTask -TaskName "YXZX-Git-AutoPush"
```

### 删除任务
```powershell
Unregister-ScheduledTask -TaskName "YXZX-Git-AutoPush" -Confirm:$false
```

## ⚙️ 修改推送时间

如需修改推送时间（例如改为凌晨 2 点）：
```powershell
$task = Get-ScheduledTask -TaskName "YXZX-Git-AutoPush"
$task.Triggers[0].At = "2:00 AM"
Set-ScheduledTask -InputObject $task
```

## 📝 注意事项

1. **Git 配置**: 首次运行会自动配置 Git 用户信息
2. **网络连接**: 推送时需要网络连接
3. **权限**: 需要有 GitHub 仓库的推送权限
4. **日志**: 日志文件只保留最近 500 行

---

*创建时间：2026-03-11*
