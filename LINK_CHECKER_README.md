# 链接检测工具使用说明

## 📋 简介

本工具用于自动检测 README.md 中所有链接的有效性，并生成详细报告。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行链接检测

```bash
python3 check_links.py
```

### 3. 查看检测报告

检测完成后会生成两个报告文件：
- `link_check_report.md` - Markdown 格式报告（人类可读）
- `link_check_report.json` - JSON 格式报告（机器可读）

### 4. 更新 README 时间戳

```bash
python3 update_readme_time.py
```

## 📁 文件说明

### check_links.py
主要链接检测脚本，功能包括：
- 从 README.md 提取所有链接
- 并发检测链接有效性（默认 10 个线程）
- 自动重试失败的链接（默认重试 2 次）
- 生成详细的检测报告

**配置参数**：
```python
TIMEOUT = 10        # 请求超时时间（秒）
MAX_WORKERS = 10    # 并发线程数
RETRY_TIMES = 2     # 重试次数
```

### update_readme_time.py
自动更新 README.md 的更新时间和链接检测状态

### link_check_report.md
Markdown 格式的检测报告，包含：
- 统计信息（总链接数、有效数、失效数、成功率）
- 失效链接列表（含错误信息）
- 有效链接列表（可折叠）

### link_check_report.json
JSON 格式的检测报告，包含完整的检测数据，便于程序处理

## 📊 检测报告示例

```
# 链接检测报告

**检测时间**: 2025-10-16 23:03:29

## 📊 统计信息

- 总链接数: 118
- ✅ 有效链接: 98
- ❌ 失效链接: 20
- 成功率: 83.05%
```

## 🔄 自动化

### 使用 Cron 定时检测（Linux/Mac）

编辑 crontab：
```bash
crontab -e
```

添加以下行（每天凌晨 2 点执行）：
```
0 2 * * * cd /path/to/project && python3 check_links.py && python3 update_readme_time.py
```

### 使用 GitHub Actions 自动检测

在 `.github/workflows/check-links.yml` 中添加：

```yaml
name: Check Links

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨 2 点
  workflow_dispatch:  # 允许手动触发

jobs:
  check-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install requests

      - name: Check links
        run: |
          python3 check_links.py
          python3 update_readme_time.py

      - name: Commit report
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add link_check_report.* README.md
          git commit -m "chore: update link check report [skip ci]" || exit 0
          git push
```

## ⚙️ 高级配置

### 自定义检测规则

在 `check_links.py` 中修改：

```python
# 排除某些域名不检测
EXCLUDED_DOMAINS = ['example.com', 'test.com']

# 自定义 User-Agent
HEADERS = {
    'User-Agent': 'Your Custom User Agent'
}

# 调整并发数和超时时间
MAX_WORKERS = 20  # 提高并发数
TIMEOUT = 15      # 延长超时时间
```

### 检测结果过滤

只检测失效的链接：
```python
failed_links = [r for r in results if r['status'] == 'failed']
```

只检测特定域名：
```python
github_links = [r for r in results if 'github.com' in r['url']]
```

## 🐛 故障排除

### 问题：部分链接检测失败
**原因**：网络问题、反爬虫机制、请求超时
**解决方案**：
1. 增加重试次数 `RETRY_TIMES`
2. 延长超时时间 `TIMEOUT`
3. 修改 User-Agent 模拟浏览器访问

### 问题：检测速度太慢
**原因**：并发数不足、网络延迟
**解决方案**：
1. 增加并发线程数 `MAX_WORKERS`
2. 使用代理加速访问

### 问题：某些网站一直显示失败
**原因**：网站反爬虫、需要登录、地区限制
**解决方案**：
1. 添加到排除列表
2. 使用更真实的请求头
3. 手动验证链接有效性

## 📝 更新日志

### v1.0.0 (2025-10-16)
- ✨ 初始版本发布
- ✅ 支持 Markdown 链接提取
- ✅ 并发链接检测
- ✅ 自动重试机制
- ✅ 生成详细报告
- ✅ 自动更新 README 时间戳

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题，请在 GitHub 上提 Issue。
