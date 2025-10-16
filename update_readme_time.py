#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新 README.md 的更新时间和链接检测状态
"""

import re
import json
from datetime import datetime


def update_readme_time():
    """更新 README.md 的更新时间"""
    readme_file = 'README.md'

    # 读取 README.md
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 尝试读取最新的链接检测报告
    link_status = ""
    try:
        with open('link_check_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
            total = report['total']
            success = report['success']
            success_rate = report['success_rate']
            link_status = f"\n> **🔗 链接检测状态**: ✅ {success}/{total} 链接有效 ({success_rate:.2f}%) - [查看完整检测报告](./link_check_report.md)"
    except FileNotFoundError:
        link_status = "\n> **🔗 链接检测状态**: ⚠️ 未检测 - [点击运行检测](./check_links.py)"

    # 匹配并替换更新时间
    pattern = r'(> \*\*📅 最近更新时间\*\*:.*?)(?:\n> \*\*🔗 链接检测状态\*\*:.*?)?(\n<p align="center">|$)'

    replacement = f'> **📅 最近更新时间**: {current_date}{link_status}\\2'

    # 如果找到匹配项，则替换
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
    else:
        # 如果没有找到，尝试在标题后添加
        title_pattern = r'(\*\*chatgptproject 持续更新，纯手工整理，欢迎 star！\*\*\n)'
        new_content = re.sub(
            title_pattern,
            f'\\1\n> **📅 最近更新时间**: {current_date}{link_status}\n',
            content
        )

    # 写回文件
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ README.md 已更新")
    print(f"   更新时间: {current_date}")
    if link_status:
        print(f"   链接检测状态已同步")


if __name__ == '__main__':
    update_readme_time()
