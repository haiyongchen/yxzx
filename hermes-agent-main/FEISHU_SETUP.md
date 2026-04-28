# 飞书机器人接入 Hermes Agent 配置指南

## ✅ 已完成配置

**Hermes Agent 配置：**
- App ID: `cli_a968bd97987bdcbd`
- App Secret: `Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0`
- 模型：qwen3.5-plus (阿里云百炼)
- 配置文件：`C:\Users\63111\.hermes\config.yaml`

---

## 📋 飞书后台配置步骤

### 1. 登录飞书开放平台
访问：https://open.feishu.cn/

### 2. 进入应用管理
- 选择你的企业
- 找到应用 `cli_a968bd97987bdcbd`
- 点击进入管理后台

### 3. 配置机器人功能
1. 点击「添加能力」→「机器人」
2. 配置机器人名称和头像

### 4. 配置事件订阅
1. 点击「事件订阅」
2. 开启事件订阅开关
3. 配置请求网址（Webhook URL）：
   ```
   http://你的服务器IP:18789/feishu/webhook
   ```
   
   **本地测试：**
   ```
   http://localhost:18789/feishu/webhook
   ```

4. 订阅以下事件：
   - `receive_message` (接收消息)
   - `message.read_receipt` (可选，消息已读)

### 5. 配置机器人发布范围
- 点击「版本管理与发布」
- 添加可访问范围（添加测试用户或全公司）
- 点击「发布」

---

## 🚀 启动 Hermes 飞书网关

### 方式 1：双击启动
```
D:\openclaw-workspace\hermes-agent-main\start_feishu_gateway.bat
```

### 方式 2：CMD 启动
```cmd
cd D:\openclaw-workspace\hermes-agent-main
start_feishu_gateway.bat
```

### 方式 3：PowerShell 启动
```powershell
cd D:\openclaw-workspace\hermes-agent-main
.\start_feishu_gateway.bat
```

---

## 🔧 高级配置

### 修改网关端口
编辑 `C:\Users\63111\.hermes\config.yaml`：
```yaml
gateway:
  feishu:
    enabled: true
    app_id: cli_a968bd97987bdcbd
    app_secret: Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0
    port: 18789  # 自定义端口
```

### 查看网关状态
```cmd
python hermes gateway status
```

### 停止网关
按 `Ctrl+C` 或关闭命令行窗口

---

## 🧪 测试

1. 启动网关后
2. 在飞书中给机器人发送消息
3. 机器人应该会通过 Hermes Agent 回复（使用百炼 qwen3.5-plus）

---

## ⚠️ 注意事项

1. **本地测试**：如果在本地运行，飞书无法访问 `localhost`，需要使用内网穿透工具（如 ngrok）
2. **公网部署**：需要配置公网 IP 和端口映射
3. **防火墙**：确保 18789 端口开放
4. **HTTPS**：生产环境建议使用 HTTPS（需要反向代理）

---

## 📞 故障排查

### 查看日志
```cmd
python hermes logs -f
```

### 检查配置
```cmd
python hermes config show
```

### 测试 API 连接
```cmd
python test_bailian.py
```
