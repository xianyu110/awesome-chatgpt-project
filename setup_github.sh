#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   GitHub 自动化设置脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查是否在 git 仓库中
if [ ! -d .git ]; then
    echo -e "${YELLOW}📁 当前不是 Git 仓库，正在初始化...${NC}"
    git init
    echo -e "${GREEN}✅ Git 仓库初始化完成${NC}"
fi

# 检查是否有远程仓库
if ! git remote | grep -q origin; then
    echo ""
    echo -e "${YELLOW}🔗 需要配置远程仓库${NC}"
    echo -e "${BLUE}请输入你的 GitHub 仓库地址（例如: https://github.com/username/repo.git）:${NC}"
    read -p "GitHub URL: " github_url

    if [ -n "$github_url" ]; then
        git remote add origin "$github_url"
        echo -e "${GREEN}✅ 远程仓库已配置: $github_url${NC}"
    else
        echo -e "${RED}❌ 未提供仓库地址，跳过此步骤${NC}"
    fi
else
    echo -e "${GREEN}✅ 已配置远程仓库: $(git remote get-url origin)${NC}"
fi

# 检查 Python 和依赖
echo ""
echo -e "${YELLOW}🐍 检查 Python 环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"

    # 检查 requests 模块
    if python3 -c "import requests" 2>/dev/null; then
        echo -e "${GREEN}✅ requests 模块已安装${NC}"
    else
        echo -e "${YELLOW}📦 正在安装 requests 模块...${NC}"
        pip3 install requests
        echo -e "${GREEN}✅ requests 模块安装完成${NC}"
    fi
else
    echo -e "${RED}❌ 未找到 Python 3，请先安装 Python${NC}"
    exit 1
fi

# 运行链接检测
echo ""
echo -e "${YELLOW}🔍 运行链接检测（这可能需要几分钟）...${NC}"
if python3 check_links.py; then
    echo -e "${GREEN}✅ 链接检测完成${NC}"
else
    echo -e "${YELLOW}⚠️  链接检测完成（部分链接失效）${NC}"
fi

# 更新 README 时间
echo ""
echo -e "${YELLOW}⏰ 更新 README 时间戳...${NC}"
python3 update_readme_time.py
echo -e "${GREEN}✅ 时间戳已更新${NC}"

# 添加并提交更改
echo ""
echo -e "${YELLOW}📝 准备提交更改...${NC}"

# 检查是否有更改
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${GREEN}✅ 没有需要提交的更改${NC}"
else
    echo -e "${BLUE}当前更改的文件:${NC}"
    git status --short

    echo ""
    echo -e "${BLUE}是否提交这些更改? (y/n)${NC}"
    read -p "提交? " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .

        # 生成提交信息
        if [ -f link_check_report.json ]; then
            FAILED=$(python3 -c "import json; print(json.load(open('link_check_report.json'))['failed'])")
            SUCCESS=$(python3 -c "import json; print(json.load(open('link_check_report.json'))['success'])")
            TOTAL=$(python3 -c "import json; print(json.load(open('link_check_report.json'))['total'])")

            COMMIT_MSG="chore: 初始化项目并更新链接检测报告

📊 检测结果:
- ✅ 有效链接: ${SUCCESS}/${TOTAL}
- ❌ 失效链接: ${FAILED}

🔧 功能更新:
- 添加自动链接检测功能
- 添加 GitHub Actions 自动化
- 优化 README 排版"
        else
            COMMIT_MSG="chore: 初始化项目"
        fi

        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✅ 更改已提交${NC}"

        # 推送到 GitHub
        if git remote | grep -q origin; then
            echo ""
            echo -e "${BLUE}是否推送到 GitHub? (y/n)${NC}"
            read -p "推送? " -n 1 -r
            echo

            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # 检查当前分支
                CURRENT_BRANCH=$(git branch --show-current)
                if [ -z "$CURRENT_BRANCH" ]; then
                    CURRENT_BRANCH="main"
                    git branch -M main
                fi

                echo -e "${YELLOW}🚀 正在推送到 $CURRENT_BRANCH 分支...${NC}"
                if git push -u origin "$CURRENT_BRANCH"; then
                    echo -e "${GREEN}✅ 推送成功！${NC}"
                else
                    echo -e "${RED}❌ 推送失败，请检查网络连接和仓库权限${NC}"
                    echo -e "${YELLOW}💡 提示: 你可能需要先在 GitHub 上创建仓库${NC}"
                fi
            fi
        fi
    else
        echo -e "${YELLOW}⏭️  跳过提交${NC}"
    fi
fi

# 显示下一步操作
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ 设置完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}📋 下一步操作:${NC}"
echo ""
echo -e "1. ${BLUE}在 GitHub 上配置 Actions 权限:${NC}"
echo -e "   进入仓库 Settings → Actions → General"
echo -e "   选择 'Read and write permissions'"
echo ""
echo -e "2. ${BLUE}手动触发第一次检测:${NC}"
echo -e "   进入仓库 Actions 页面"
echo -e "   点击 'Auto Update Links and Timestamp'"
echo -e "   点击 'Run workflow'"
echo ""
echo -e "3. ${BLUE}查看检测报告:${NC}"
echo -e "   cat link_check_report.md"
echo ""
echo -e "4. ${BLUE}查看详细使用说明:${NC}"
echo -e "   cat GITHUB_SETUP.md"
echo ""
echo -e "${GREEN}🎉 自动化已配置完成，将每天自动检测链接！${NC}"
echo ""

# 显示仓库 URL
if git remote | grep -q origin; then
    REPO_URL=$(git remote get-url origin)
    echo -e "${BLUE}📦 你的仓库地址: ${NC}$REPO_URL"

    # 将 .git 结尾的 URL 转换为网页 URL
    WEB_URL=$(echo "$REPO_URL" | sed 's/\.git$//')
    if [[ $WEB_URL == https://* ]]; then
        echo -e "${BLUE}🌐 网页访问: ${NC}$WEB_URL"
        echo -e "${BLUE}📊 Actions 页面: ${NC}${WEB_URL}/actions"
    fi
fi

echo ""
