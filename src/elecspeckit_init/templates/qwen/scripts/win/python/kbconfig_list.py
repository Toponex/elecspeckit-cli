#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kbconfig_list.py - 列出知识源条目

支持按类别筛选和查看详情 (per FR-017, T054d):
- 列出所有类别的条目
- 按类别筛选
- 显示启用状态和占位符
- 显示统计信息

Usage:
    # 列出所有知识源
    python kbconfig_list.py --config .elecspecify/memory/knowledge-sources.json

    # 列出特定类别
    python kbconfig_list.py --config knowledge-sources.json --category standards

    # 仅列出启用的条目
    python kbconfig_list.py --config knowledge-sources.json --enabled-only

Exit codes:
    0: 列出成功
    1: 列出失败
"""

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


VALID_CATEGORIES = ["standards", "company_kb", "reference_designs", "web"]


def load_config(config_path: Path) -> Dict[str, Any]:
    """加载配置文件"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件不存在: {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败: {e}", file=sys.stderr)
        sys.exit(1)


def contains_placeholder(value: Any) -> bool:
    """检查值是否包含 {{PLACEHOLDER: 字符串"""
    if isinstance(value, str):
        return "{{PLACEHOLDER:" in value or "{{PLACEHOLDER" in value
    elif isinstance(value, dict):
        return any(contains_placeholder(v) for v in value.values())
    elif isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    return False


def contains_env_reference(value: Any) -> bool:
    """检查值是否包含 ENV: 引用"""
    if isinstance(value, str):
        return value.startswith("ENV:")
    elif isinstance(value, dict):
        return any(contains_env_reference(v) for v in value.values())
    elif isinstance(value, list):
        return any(contains_env_reference(item) for item in value)
    return False


def format_entry_summary(entry: Dict[str, Any], category: str) -> str:
    """格式化条目摘要"""
    entry_id = entry.get("id", "unknown")
    enabled = entry.get("enabled", False)
    status = "✓" if enabled else "✗"

    # 类别特定信息
    info_parts = []

    if category == "standards":
        standard_number = entry.get("standard_number", "")
        year = entry.get("year", "")
        title = entry.get("title", "")
        deprecated = entry.get("deprecated", False)

        info_parts.append(f"{standard_number} ({year})")
        if title:
            info_parts.append(f"- {title}")
        if deprecated:
            info_parts.append("[已废弃]")

    elif category == "company_kb":
        doc_type = entry.get("type", "")
        title = entry.get("title", "")
        year = entry.get("year", "")
        authors = entry.get("authors", [])

        if title:
            info_parts.append(title)
        if doc_type:
            info_parts.append(f"({doc_type})")
        if year:
            info_parts.append(f"{year}")
        if authors:
            info_parts.append(f"作者: {', '.join(authors)}")

    elif category == "reference_designs":
        name = entry.get("name", "")
        vendor = entry.get("vendor", "")
        url = entry.get("url", "")

        if name:
            info_parts.append(name)
        if vendor:
            info_parts.append(f"({vendor})")
        if url:
            info_parts.append(f"URL: {url}")

    elif category == "web":
        name = entry.get("name", "")
        url = entry.get("url", "")
        api_key = entry.get("api_key", "")

        if name:
            info_parts.append(name)
        if url:
            info_parts.append(f"URL: {url}")

        # API 密钥状态
        if api_key:
            if contains_placeholder(api_key):
                info_parts.append("[API密钥: 占位符]")
            elif api_key.startswith("ENV:"):
                info_parts.append(f"[API密钥: {api_key}]")
            else:
                info_parts.append("[API密钥: 已配置]")

    # 检查占位符和 ENV 引用
    flags = []
    if contains_placeholder(entry):
        flags.append("含占位符")
    if contains_env_reference(entry):
        flags.append("ENV引用")

    info_str = " ".join(info_parts)
    flags_str = f" ({', '.join(flags)})" if flags else ""

    return f"  {status} [{entry_id}] {info_str}{flags_str}"


def list_category(category: str, data: Dict[str, Any], enabled_only: bool = False) -> int:
    """
    列出指定类别的条目

    Returns:
        条目数量
    """
    if category not in data:
        print(f"错误: 类别 '{category}' 不存在", file=sys.stderr)
        return 0

    cat_data = data[category]
    cat_enabled = cat_data.get("enabled", False)
    sources = cat_data.get("sources", [])

    # 应用筛选
    if enabled_only:
        sources = [s for s in sources if isinstance(s, dict) and s.get("enabled", False)]

    # 统计信息
    total_count = len(sources)
    enabled_count = sum(1 for s in sources if isinstance(s, dict) and s.get("enabled", False))
    placeholder_count = sum(1 for s in sources if isinstance(s, dict) and contains_placeholder(s))

    # 打印类别标题
    cat_status = "启用" if cat_enabled else "禁用"
    print(f"\n{category.upper()} ({cat_status})")
    print(f"  总计: {total_count} 个条目 ({enabled_count} 已启用, {placeholder_count} 包含占位符)")
    print()

    # 打印条目
    if not sources:
        print("  (无条目)")
        return 0

    for entry in sources:
        if not isinstance(entry, dict):
            continue

        summary = format_entry_summary(entry, category)
        print(summary)

    return total_count


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="列出知识源条目", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument("--category", choices=VALID_CATEGORIES, help="筛选指定类别")
    parser.add_argument("--enabled-only", action="store_true", help="仅显示已启用的条目")

    args = parser.parse_args()

    # 加载配置
    data = load_config(args.config)

    # 确定要列出的类别
    categories = [args.category] if args.category else VALID_CATEGORIES

    # 打印标题
    print(f"知识源配置: {args.config}")

    # 列出类别
    total_entries = 0
    for category in categories:
        count = list_category(category, data, args.enabled_only)
        total_entries += count

    # 打印总结
    print()
    print(f"总计: {total_entries} 个条目")


if __name__ == "__main__":
    main()
