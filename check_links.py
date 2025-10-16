#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接检测脚本
检测 README.md 中所有链接的有效性
"""

import re
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import time

# 配置
TIMEOUT = 10  # 请求超时时间（秒）
MAX_WORKERS = 10  # 并发线程数
RETRY_TIMES = 2  # 重试次数

# 用户代理，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_links_from_markdown(file_path):
    """从 Markdown 文件中提取所有链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 Markdown 链接格式 [text](url)
    markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

    # 匹配纯 URL
    url_pattern = r'https?://[^\s\)\]\>]+'
    plain_urls = re.findall(url_pattern, content)

    # 合并并去重
    all_links = {}

    # 添加 Markdown 格式的链接
    for text, url in markdown_links:
        if url.startswith('http'):
            all_links[url] = text

    # 添加纯 URL（使用 URL 本身作为文本）
    for url in plain_urls:
        if url not in all_links:
            all_links[url] = url

    return all_links

def check_url(url, retry=RETRY_TIMES):
    """检查单个 URL 的有效性"""
    for attempt in range(retry + 1):
        try:
            # 对于某些特殊域名，使用 HEAD 请求
            response = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)

            # 如果 HEAD 请求失败，尝试 GET 请求
            if response.status_code >= 400:
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)

            status_code = response.status_code

            if status_code < 400:
                return {
                    'url': url,
                    'status': 'success',
                    'status_code': status_code,
                    'message': 'OK'
                }
            else:
                return {
                    'url': url,
                    'status': 'failed',
                    'status_code': status_code,
                    'message': f'HTTP {status_code}'
                }

        except requests.exceptions.Timeout:
            if attempt < retry:
                time.sleep(1)
                continue
            return {
                'url': url,
                'status': 'failed',
                'status_code': None,
                'message': 'Timeout'
            }
        except requests.exceptions.ConnectionError:
            if attempt < retry:
                time.sleep(1)
                continue
            return {
                'url': url,
                'status': 'failed',
                'status_code': None,
                'message': 'Connection Error'
            }
        except Exception as e:
            return {
                'url': url,
                'status': 'failed',
                'status_code': None,
                'message': str(e)
            }

    return {
        'url': url,
        'status': 'failed',
        'status_code': None,
        'message': 'Max retries reached'
    }

def check_links(links_dict):
    """批量检测链接"""
    results = []
    total = len(links_dict)

    print(f"开始检测 {total} 个链接...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(check_url, url): (url, text)
            for url, text in links_dict.items()
        }

        completed = 0
        for future in as_completed(future_to_url):
            url, text = future_to_url[future]
            try:
                result = future.result()
                result['text'] = text
                results.append(result)

                completed += 1
                # 显示进度
                status_icon = '✓' if result['status'] == 'success' else '✗'
                print(f"[{completed}/{total}] {status_icon} {url[:80]}...")

            except Exception as e:
                results.append({
                    'url': url,
                    'text': text,
                    'status': 'failed',
                    'status_code': None,
                    'message': str(e)
                })

    return results

def generate_report(results, output_file='link_check_report.md'):
    """生成检测报告"""
    success_count = sum(1 for r in results if r['status'] == 'success')
    failed_count = len(results) - success_count
    success_rate = (success_count / len(results) * 100) if results else 0

    # 按状态分类
    failed_links = [r for r in results if r['status'] == 'failed']

    # 生成 Markdown 报告
    report = f"""# 链接检测报告

**检测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 统计信息

- 总链接数: {len(results)}
- ✅ 有效链接: {success_count}
- ❌ 失效链接: {failed_count}
- 成功率: {success_rate:.2f}%

---

## ❌ 失效链接列表

"""

    if failed_links:
        report += "| 序号 | 链接文本 | URL | 错误信息 |\n"
        report += "|------|---------|-----|----------|\n"

        for idx, link in enumerate(failed_links, 1):
            text = link['text'][:50] + '...' if len(link['text']) > 50 else link['text']
            url = link['url'][:80] + '...' if len(link['url']) > 80 else link['url']
            message = link['message']
            report += f"| {idx} | {text} | {url} | {message} |\n"
    else:
        report += "🎉 所有链接都有效！\n"

    report += "\n---\n\n## ✅ 有效链接列表\n\n"

    success_links = [r for r in results if r['status'] == 'success']
    if success_links:
        report += f"共 {len(success_links)} 个有效链接\n\n"
        report += "<details>\n<summary>点击展开查看</summary>\n\n"
        report += "| 序号 | 链接文本 | URL | 状态码 |\n"
        report += "|------|---------|-----|--------|\n"

        for idx, link in enumerate(success_links, 1):
            text = link['text'][:50] + '...' if len(link['text']) > 50 else link['text']
            url = link['url'][:80] + '...' if len(link['url']) > 80 else link['url']
            status_code = link.get('status_code', 'N/A')
            report += f"| {idx} | {text} | {url} | {status_code} |\n"

        report += "\n</details>\n"

    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ 报告已生成: {output_file}")

    # 同时保存 JSON 格式
    json_file = output_file.replace('.md', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'check_time': datetime.now().isoformat(),
            'total': len(results),
            'success': success_count,
            'failed': failed_count,
            'success_rate': success_rate,
            'results': results
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON 报告已生成: {json_file}")

    return success_count, failed_count

def main():
    """主函数"""
    readme_file = 'README.md'

    print("=" * 60)
    print("README.md 链接检测工具")
    print("=" * 60)
    print()

    # 提取链接
    print("📝 正在提取链接...")
    links = extract_links_from_markdown(readme_file)
    print(f"✅ 提取到 {len(links)} 个链接\n")

    # 检测链接
    results = check_links(links)

    # 生成报告
    print("\n" + "=" * 60)
    print("📊 生成检测报告...")
    success, failed = generate_report(results)

    print("\n" + "=" * 60)
    print(f"✅ 检测完成!")
    print(f"   有效: {success} | 失效: {failed}")
    print("=" * 60)

if __name__ == '__main__':
    main()
