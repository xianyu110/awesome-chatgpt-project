# 如何上传到 GitHub 并保持自动更新

## 📋 目录
- [快速开始](#快速开始)
- [GitHub 自动化配置](#github-自动化配置)
- [手动操作指南](#手动操作指南)
- [高级配置](#高级配置)

---

## 🚀 快速开始

### 1. 初始化 Git 仓库（如果还没有）

```bash
cd /Users/chinamanor/Downloads/cursor编程/awesome-chatgpt-project

# 初始化 git
git init

# 添加所有文件
git add .

# 创建首次提交
git commit -m "feat: 初始化项目并添加自动链接检测功能"
```

### 2. 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `awesome-chatgpt-project`
   - **Description**: 最新最火的 ChatGPT 项目合集
   - **Public** 或 **Private**（建议 Public）
   - ❌ 不要勾选 "Initialize with README"（因为本地已有）

3. 点击 **Create repository**

### 3. 连接到 GitHub 并推送

```bash
# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/awesome-chatgpt-project.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 4. 启用 GitHub Actions

GitHub Actions 会自动启用，但需要配置权限：

1. 进入仓库页面
2. 点击 **Settings** → **Actions** → **General**
3. 在 **Workflow permissions** 中选择：
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. 点击 **Save**

---

## 🤖 GitHub 自动化配置

已为你创建了 `.github/workflows/auto-update.yml`，它会：

### ✨ 功能特性

1. **自动定时检测**
   - 每天北京时间上午 9 点自动运行
   - 检测所有链接的有效性

2. **自动更新**
   - 更新 README.md 的时间戳
   - 生成最新的链接检测报告
   - 自动提交并推送到 GitHub

3. **失效链接提醒**
   - 当发现失效链接时，自动创建 Issue
   - Issue 中包含详细的失效链接列表
   - 自动打上 `automated` 和 `links` 标签

4. **手动触发**
   - 可以随时在 GitHub Actions 页面手动触发

### 📅 运行时间设置

在 `.github/workflows/auto-update.yml` 中：

```yaml
schedule:
  # 每天北京时间上午 9 点（UTC 1:00）
  - cron: '0 1 * * *'
```

**Cron 时间说明**：
- `0 1 * * *` - 每天 UTC 1:00（北京时间 9:00）
- `0 2 * * 0` - 每周日 UTC 2:00（北京时间 10:00）
- `0 */6 * * *` - 每 6 小时一次
- `0 0 1 * *` - 每月 1 号

### 🔧 修改运行频率

编辑 `.github/workflows/auto-update.yml`：

```yaml
on:
  schedule:
    # 每 12 小时一次
    - cron: '0 */12 * * *'

    # 每周一次
    - cron: '0 2 * * 1'

    # 每月一次
    - cron: '0 2 1 * *'
```

---

## 📖 手动操作指南

### 手动检测链接

```bash
# 在本地运行
python3 check_links.py

# 更新 README 时间
python3 update_readme_time.py

# 提交更改
git add .
git commit -m "chore: 更新链接检测报告"
git push
```

### 查看 GitHub Actions 运行状态

1. 进入你的 GitHub 仓库
2. 点击 **Actions** 标签
3. 查看运行历史和日志

### 手动触发 GitHub Actions

1. 进入 **Actions** 标签
2. 点击左侧的 **Auto Update Links and Timestamp**
3. 点击右上角的 **Run workflow**
4. 选择分支并点击 **Run workflow**

---

## ⚙️ 高级配置

### 1. 配置通知

#### Slack 通知

在 `.github/workflows/auto-update.yml` 中添加：

```yaml
- name: Send Slack notification
  if: steps.changes.outputs.has_changes == 'true'
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "链接检测完成",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*链接检测报告*\n失效链接: ${{ env.FAILED_COUNT }}\n有效链接: ${{ env.SUCCESS_COUNT }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### 邮件通知

添加 secrets：
1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 添加以下 secrets：
   - `EMAIL_USERNAME` - 你的邮箱
   - `EMAIL_PASSWORD` - 邮箱密码或应用专用密码

然后在 workflow 中添加：

```yaml
- name: Send email notification
  if: steps.changes.outputs.has_changes == 'true'
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 链接检测报告 - ${{ github.repository }}
    body: 检测到 ${{ env.FAILED_COUNT }} 个失效链接
    to: your-email@example.com
    from: GitHub Actions
```

### 2. 自动修复某些链接

创建 `fix_links.py`：

```python
#!/usr/bin/env python3
"""自动修复已知的链接问题"""

LINK_REPLACEMENTS = {
    'http://old-domain.com': 'https://new-domain.com',
    'https://broken-link.com': 'https://working-link.com',
}

def fix_links():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in LINK_REPLACEMENTS.items():
        content = content.replace(old, new)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_links()
```

在 workflow 中添加：

```yaml
- name: Auto fix known issues
  run: |
    python3 fix_links.py
```

### 3. 添加 Badge 到 README

在 README.md 顶部添加：

```markdown
[![Link Check](https://github.com/YOUR_USERNAME/awesome-chatgpt-project/actions/workflows/auto-update.yml/badge.svg)](https://github.com/YOUR_USERNAME/awesome-chatgpt-project/actions/workflows/auto-update.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Last Update](https://img.shields.io/github/last-commit/YOUR_USERNAME/awesome-chatgpt-project)](https://github.com/YOUR_USERNAME/awesome-chatgpt-project/commits/main)
```

### 4. 设置 PR 自动合并

如果想要自动合并 GitHub Actions 创建的 PR：

```yaml
- name: Enable auto-merge for bot PRs
  if: steps.changes.outputs.has_changes == 'true'
  run: |
    gh pr create --title "自动更新链接检测报告" \
                 --body "🤖 由 GitHub Actions 自动创建" \
                 --base main --head auto-update
    gh pr merge --auto --merge
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🐛 故障排除

### 问题 1: GitHub Actions 权限不足

**错误信息**: `permission denied` 或 `403 Forbidden`

**解决方案**:
1. 进入 **Settings** → **Actions** → **General**
2. 设置 **Workflow permissions** 为 **Read and write permissions**

### 问题 2: Push 失败

**错误信息**: `failed to push some refs`

**解决方案**:
```bash
# 拉取最新更改
git pull origin main --rebase

# 再次推送
git push origin main
```

### 问题 3: Actions 没有自动运行

**原因**:
- 首次推送需要手动启用 Actions
- Cron 任务在仓库无活动时可能暂停

**解决方案**:
1. 手动触发一次 workflow
2. 确保仓库最近有活动

### 问题 4: Issue 创建失败

**原因**: 需要 GitHub CLI 权限

**解决方案**:
确保 workflow 中有：
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📊 监控和统计

### 查看历史检测数据

```bash
# 查看所有检测报告
git log --all --grep="自动更新链接检测报告" --oneline

# 查看某次检测的详细信息
git show <commit-hash>:link_check_report.json
```

### 生成统计图表

可以使用 GitHub Actions 生成统计图表：

```yaml
- name: Generate statistics
  run: |
    python3 generate_stats.py
```

---

## 🎯 最佳实践

1. **定期检查 Issues**
   - 及时处理自动创建的 Issue
   - 修复或删除失效链接

2. **保持脚本更新**
   - 定期更新 Python 依赖
   - 优化检测逻辑

3. **备份重要数据**
   - 定期导出检测报告
   - 保存历史统计数据

4. **优化检测频率**
   - 根据链接变化频率调整
   - 避免过于频繁的检测

---

## 📝 完整操作流程

### 首次设置

```bash
# 1. 初始化并提交
git init
git add .
git commit -m "feat: 初始化项目"

# 2. 创建 GitHub 仓库并推送
git remote add origin https://github.com/YOUR_USERNAME/awesome-chatgpt-project.git
git push -u origin main

# 3. 配置 GitHub Actions 权限
# 在 GitHub 网页端设置 Settings → Actions → General

# 4. 测试自动化
# 在 Actions 页面手动触发一次
```

### 日常维护

```bash
# 本地测试
python3 check_links.py

# 查看报告
cat link_check_report.md

# 提交更改
git add .
git commit -m "fix: 修复失效链接"
git push

# GitHub Actions 会自动运行
```

---

## 🔗 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)
- [GitHub CLI 文档](https://cli.github.com/)

---

## 📮 需要帮助？

如有问题，请：
1. 查看 GitHub Actions 运行日志
2. 检查本文档的故障排除部分
3. 在仓库中创建 Issue

---

**祝你使用愉快！🎉**
