# 腾讯文档访问经验

## 日期：2026-03-12

## 经验总结

腾讯文档 (docs.qq.com) 无法通过简单 HTTP 请求直接获取表格数据：

### 尝试过的方法（均失败）
1. **直接 HTTP 请求** - 能获取 HTML 但表格数据是动态加载的
2. **API 端点** - `/api/doc/`, `/api/tabs/`, `/api/sheet/*/data` 等都返回 404
3. **HTML 解析** - 页面使用 JavaScript 动态渲染，HTML 中无完整表格数据
4. **Playwright/Selenium** - 需要下载浏览器且网络问题导致失败

### 可行方案
1. **用户手动导出** - 请用户点击 ⋮ → 导出为 → Excel
2. **用户复制粘贴** - 请用户复制表格内容
3. **使用已打开的浏览器** - 如果用户已在 Chrome 中打开，可尝试通过浏览器扩展或开发者工具提取

### 后续处理原则
- 遇到腾讯文档链接，先尝试直接访问
- 如果无法获取数据，请用户导出 Excel 或复制内容
- 不要花费过多时间尝试突破登录验证

## 相关文件
- `D:\openclaw-workspace\fetch_qq_direct.py` - 直接请求测试
- `D:\openclaw-workspace\try_api.py` - API 端点测试
- `D:\openclaw-workspace\parse_qq_doc.py` - HTML 解析测试
