# 🍊 HK Ticketing 半自动抢票助手

## 安装步骤

### 1. 安装 Tampermonkey 浏览器扩展

| 浏览器 | 安装地址 |
|--------|---------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) |
| Edge | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/firefox/addon/tampermonkey/) |

### 2. 安装脚本

1. 点击浏览器中的 Tampermonkey 图标 → **添加新脚本**
2. 清空编辑器内容
3. 把 `hkt-ticket-helper.user.js` 的全部内容粘贴进去
4. 按 `Ctrl + S` 保存

### 3. 配置脚本

打开脚本编辑器，修改 `CONFIG` 部分：

```javascript
const CONFIG = {
    // 改成你要抢的项目 ID（从 URL 获取）
    projectId: '50000001244002',

    // 改成实际开票时间
    saleStartTime: '2026-05-25T10:00:00+08:00',

    // 你想要的票档（按优先级排列，关键词要和页面上显示的一致）
    preferZones: ['VIP', 'A区', 'B区'],

    // 购买数量
    ticketCount: 2,

    // 购票人信息
    buyerInfo: {
        name: '张三',
        phone: '13800138000',
        email: 'your@email.com',
        idNumber: 'H12345678',
    },

    // true = 自动提交（激进），false = 填好后等你手动提交（推荐）
    autoSubmit: false,
};
```

### 4. 使用流程

1. **提前 30 分钟**打开目标页面 `https://hkt.hkticketing.com/#/allEvents/detail?projectId=50000001244002`
2. **提前登录**你的账号（确保 cookie 是活的）
3. 页面右上角会出现 **🍊 抢票助手** 面板
4. 点 **🔍 分析页面结构** → 按 F12 看控制台输出
5. 根据控制台输出的按钮/输入框信息，**调整脚本中的选择器**
6. 到点了点 **🚀 开始抢票**

### 5. 关键：抓包分析

脚本里的选择器是通用猜测，**你一定要用 F12 抓包确认真实的选择器**：

1. 按 `F12` 打开开发者工具
2. 切到 **Network（网络）** 标签
3. 刷新页面，观察加载了哪些 `api`、`ticket`、`order` 相关的请求
4. 切到 **Elements（元素）** 标签
5. 用左上角的选择工具（🔍）点击页面上的：
   - 票档区域 → 记下 class 名 → 改到 `selectZone()` 里
   - 数量选择器 → 记下 class/id → 改到 `selectQuantity()` 里
   - 提交按钮 → 记下 class → 改到 `submitOrder()` 里

**控制台里标记为 `[XHR]` 和 `[Fetch]` 的请求就是 API 接口**，这些信息很重要！

## 工作原理

```
开票前 30 秒 → 自动刷新页面（每 2 秒一次）
开票前 5 秒  → 高频刷新（每 0.5 秒一次）
开票后       → 自动执行：
                ① 选择票档（按你设定的优先级）
                ② 设置数量
                ③ 填写购票人信息
                ④ 高亮/自动提交（取决于 autoSubmit 设置）
```

## 注意事项

- 脚本在你的浏览器里运行，使用你自己的登录态，不需要额外处理 cookie
- 首次使用建议先 **不开 autoSubmit**，跑一遍流程看看对不对
- 如果平台有验证码，需要你手动处理（脚本无法绕过）
- 平台可能会更新前端结构，选择器可能需要定期维护
- 请遵守平台规则，合理使用
