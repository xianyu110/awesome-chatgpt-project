# 📦 项目文件结构

```
awesome-chatgpt-project/
├── README.md                          # 主文档（已优化排版）
├── .github/
│   └── workflows/
│       └── auto-update.yml           # GitHub Actions 自动化配置
├── check_links.py                     # 链接检测脚本
├── update_readme_time.py              # 时间更新脚本
├── setup_github.sh                    # 一键配置脚本
├── link_check_report.md               # 检测报告（Markdown）
├── link_check_report.json             # 检测报告（JSON）
├── QUICK_START.md                     # 快速开始指南
├── GITHUB_SETUP.md                    # GitHub 详细设置指南
├── LINK_CHECKER_README.md             # 链接检测工具说明
└── .gitignore                         # Git 忽略文件配置
```

---

## 🎯 核心功能

### 1. 自动链接检测
- **文件**: `check_links.py`
- **功能**: 批量检测 README.md 中所有链接的有效性
- **特性**:
  - ✅ 并发检测（10 线程）
  - ✅ 自动重试（2 次）
  - ✅ 超时控制（10 秒）
  - ✅ 生成详细报告

### 2. 自动更新时间戳
- **文件**: `update_readme_time.py`
- **功能**: 自动更新 README.md 的更新日期
- **特性**:
  - ✅ 实时日期
  - ✅ 同步链接检测状态
  - ✅ 保持格式一致

### 3. GitHub Actions 自动化
- **文件**: `.github/workflows/auto-update.yml`
- **功能**: 每天自动运行检测并更新
- **特性**:
  - ✅ 定时运行（每天 9:00）
  - ✅ 手动触发
  - ✅ 自动提交推送
  - ✅ 失效链接创建 Issue

### 4. 一键配置脚本
- **文件**: `setup_github.sh`
- **功能**: 自动化配置整个项目
- **特性**:
  - ✅ 检查环境
  - ✅ 安装依赖
  - ✅ 初始化 Git
  - ✅ 推送到 GitHub

---

## 🚀 使用流程

### 首次设置

```bash
# 方法 1: 使用自动化脚本（推荐）
./setup_github.sh

# 方法 2: 手动设置
# 1. 在 GitHub 创建仓库
# 2. 本地初始化
git init
git add .
git commit -m "feat: 初始化项目"
git remote add origin https://github.com/YOUR_USERNAME/awesome-chatgpt-project.git
git push -u origin main

# 3. 在 GitHub 上配置 Actions 权限
# Settings → Actions → General → Read and write permissions
```

### 日常使用

项目配置完成后，**完全自动化**，无需任何手动操作：

1. ✅ 每天自动检测所有链接
2. ✅ 自动更新时间戳和状态
3. ✅ 自动生成检测报告
4. ✅ 自动提交并推送到 GitHub
5. ✅ 发现失效链接自动创建 Issue

### 手动操作（可选）

```bash
# 手动检测链接
python3 check_links.py

# 手动更新时间
python3 update_readme_time.py

# 查看报告
cat link_check_report.md

# 提交更改
git add .
git commit -m "chore: 更新链接检测报告"
git push
```

---

## 📊 检测报告说明

### Markdown 报告 (link_check_report.md)
```markdown
# 链接检测报告

**检测时间**: 2025-10-16 23:03:29

## 📊 统计信息
- 总链接数: 118
- ✅ 有效链接: 98
- ❌ 失效链接: 20
- 成功率: 83.05%

## ❌ 失效链接列表
[详细的失效链接表格]

## ✅ 有效链接列表
[可折叠的有效链接表格]
```

### JSON 报告 (link_check_report.json)
```json
{
  "check_time": "2025-10-16T23:03:29",
  "total": 118,
  "success": 98,
  "failed": 20,
  "success_rate": 83.05,
  "results": [...]
}
```

---

## 🔧 配置说明

### 修改检测频率

编辑 `.github/workflows/auto-update.yml`:

```yaml
schedule:
  # 每天一次
  - cron: '0 1 * * *'

  # 每 12 小时一次
  # - cron: '0 */12 * * *'

  # 每周一次
  # - cron: '0 2 * * 0'
```

### 调整检测参数

编辑 `check_links.py`:

```python
TIMEOUT = 10        # 请求超时（秒）
MAX_WORKERS = 10    # 并发线程数
RETRY_TIMES = 2     # 重试次数
```

### 排除特定域名

```python
# 在 check_links.py 中添加
EXCLUDED_DOMAINS = [
    'example.com',
    'test.com'
]
```

---

## 📈 运行状态监控

### 查看 GitHub Actions 状态

1. 访问仓库页面
2. 点击 **Actions** 标签
3. 查看运行历史

### 查看自动创建的 Issue

1. 访问 **Issues** 页面
2. 筛选标签 `automated` 和 `links`

### 添加状态徽章

在 README.md 中添加：

```markdown
[![Link Check](https://github.com/YOUR_USERNAME/awesome-chatgpt-project/actions/workflows/auto-update.yml/badge.svg)](https://github.com/YOUR_USERNAME/awesome-chatgpt-project/actions/workflows/auto-update.yml)
```

---

## 🎨 自定义功能

### 添加通知

#### Slack 通知
在 workflow 中添加 Slack webhook 配置

#### 邮件通知
配置 SMTP 发送检测结果邮件

#### 微信通知
集成企业微信机器人推送消息

### 自动修复链接

创建 `fix_links.py` 自动替换已知的失效链接

### 生成统计图表

添加 `generate_stats.py` 生成历史统计图表

---

## 🐛 故障排除

### Actions 没有运行
- 检查 Workflow permissions
- 手动触发一次
- 确认 cron 表达式正确

### Push 失败
```bash
git pull origin main --rebase
git push origin main
```

### 链接检测失败
- 增加超时时间
- 增加重试次数
- 检查网络连接

---

## 📚 文档索引

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [QUICK_START.md](./QUICK_START.md) | 快速开始指南 | 首次配置 |
| [GITHUB_SETUP.md](./GITHUB_SETUP.md) | 详细设置指南 | 深入配置 |
| [LINK_CHECKER_README.md](./LINK_CHECKER_README.md) | 检测工具说明 | 工具使用 |
| [link_check_report.md](./link_check_report.md) | 最新检测报告 | 查看结果 |

---

## 🎉 优势特性

### 完全自动化
- ❌ 无需手动检测链接
- ❌ 无需手动更新时间
- ❌ 无需手动提交代码
- ✅ 一切都是自动的！

### 智能提醒
- 失效链接自动创建 Issue
- 详细的错误信息
- 便于快速修复

### 历史追踪
- Git 记录每次检测
- 可查看历史变化
- 便于分析趋势

### 灵活配置
- 可调整检测频率
- 可自定义检测参数
- 支持多种通知方式

---

## 🔗 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Python Requests 文档](https://requests.readthedocs.io/)
- [Cron 表达式生成器](https://crontab.guru/)
- [Markdown 语法](https://www.markdownguide.org/)

---

## 📊 项目统计

- **总文件数**: 12
- **Python 脚本**: 3
- **文档文件**: 5
- **配置文件**: 2
- **Shell 脚本**: 1

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
chore: 其他改动
```

---

## 📄 许可证

MIT License

---

## 📮 获取帮助

1. 查看文档（上方文档索引）
2. 查看 GitHub Issues
3. 查看 Actions 运行日志
4. 创建新 Issue 求助

---

**祝使用愉快！🚀**
