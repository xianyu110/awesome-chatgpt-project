# 🚀 快速上传到 GitHub

## 方法一：使用自动化脚本（推荐）⭐

```bash
# 一键配置并上传
./setup_github.sh
```

这个脚本会自动：
- ✅ 初始化 Git 仓库
- ✅ 安装依赖
- ✅ 运行链接检测
- ✅ 提交更改
- ✅ 推送到 GitHub

---

## 方法二：手动配置

### 1️⃣ 在 GitHub 创建仓库

访问 https://github.com/new 创建新仓库：
- 仓库名：`awesome-chatgpt-project`
- 可见性：Public
- ❌ 不要勾选 "Initialize with README"

### 2️⃣ 本地初始化并推送

```bash
# 初始化 Git
git init
git add .
git commit -m "feat: 初始化项目"

# 连接到 GitHub（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/awesome-chatgpt-project.git

# 推送
git branch -M main
git push -u origin main
```

### 3️⃣ 配置 GitHub Actions

1. 进入仓库 **Settings**
2. 点击 **Actions** → **General**
3. 在 **Workflow permissions** 中：
   - ✅ 选择 **Read and write permissions**
   - ✅ 勾选 **Allow GitHub Actions to create and approve pull requests**
4. 点击 **Save**

### 4️⃣ 手动触发首次运行

1. 进入仓库的 **Actions** 页面
2. 点击 **Auto Update Links and Timestamp**
3. 点击 **Run workflow**
4. 选择 `main` 分支并运行

---

## ✨ 自动化功能

配置完成后，系统将自动：

### 📅 每天自动检测
- **时间**：每天北京时间上午 9:00
- **内容**：检测所有链接有效性
- **结果**：自动生成检测报告

### 📝 自动更新
- 更新 README.md 的时间戳
- 更新链接检测状态
- 自动提交并推送更改

### 🚨 失效提醒
- 发现失效链接时自动创建 Issue
- Issue 包含详细的失效链接列表
- 自动添加标签便于管理

### 🎯 手动触发
- 随时可在 Actions 页面手动运行
- 适合紧急更新或测试

---

## 📊 如何查看结果

### 查看检测报告
```bash
# 本地查看
cat link_check_report.md

# 或在 GitHub 仓库中直接查看
https://github.com/YOUR_USERNAME/awesome-chatgpt-project/blob/main/link_check_report.md
```

### 查看运行日志
1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择任意运行记录查看详细日志

### 查看自动创建的 Issues
1. 进入 **Issues** 页面
2. 查看带有 `automated` 标签的 Issue

---

## 🔧 修改运行频率

编辑 `.github/workflows/auto-update.yml`：

```yaml
on:
  schedule:
    # 每天一次（默认）
    - cron: '0 1 * * *'

    # 每 12 小时一次
    # - cron: '0 */12 * * *'

    # 每周一次
    # - cron: '0 2 * * 0'

    # 每月一次
    # - cron: '0 2 1 * *'
```

**Cron 时间对照表**：
- `0 1 * * *` = 每天 UTC 1:00（北京时间 9:00）
- `0 13 * * *` = 每天 UTC 13:00（北京时间 21:00）
- `0 */6 * * *` = 每 6 小时
- `0 2 * * 0` = 每周日 UTC 2:00

---

## 🐛 常见问题

### Q: Push 失败怎么办？
```bash
# 先拉取远程更改
git pull origin main --rebase

# 再推送
git push origin main
```

### Q: Actions 没有自动运行？
- 检查 Workflow permissions 是否正确配置
- 手动触发一次测试
- 确认 `.github/workflows/auto-update.yml` 文件存在

### Q: 如何停止自动运行？
1. 进入 **Settings** → **Actions** → **General**
2. 选择 **Disable actions**

或删除 `.github/workflows/auto-update.yml` 文件

### Q: 如何本地测试？
```bash
# 安装依赖
pip3 install requests

# 运行检测
python3 check_links.py

# 更新时间
python3 update_readme_time.py
```

---

## 📚 详细文档

- **完整设置指南**：[GITHUB_SETUP.md](./GITHUB_SETUP.md)
- **链接检测工具**：[LINK_CHECKER_README.md](./LINK_CHECKER_README.md)
- **GitHub Actions 配置**：[.github/workflows/auto-update.yml](.github/workflows/auto-update.yml)

---

## 🎉 完成！

配置完成后，你的项目将：
- ✅ 每天自动检测所有链接
- ✅ 自动更新时间戳
- ✅ 自动提交检测报告
- ✅ 失效链接自动提醒

**完全自动化，无需人工干预！** 🚀
