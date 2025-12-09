#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kbconfig_update.py - 更新知识源条目字段

支持更新现有条目的字段 (per FR-017, T054c):
- 替换占位符为实际值
- 更新 ENV 引用格式
- 启用/禁用条目
- 修改任意字段

Usage:
    # 配置 Metaso API 密钥并启用
    python kbconfig_update.py --category web --id metaso \\
        --api_key "ENV:METASO_API_KEY" --enabled true \\
        --config .elecspecify/memory/knowledge-sources.json

    # 禁用某个标准
    python kbconfig_update.py --category standards --id IPC-2221B \\
        --enabled false --config knowledge-sources.json

    # 更新标准年份
    python kbconfig_update.py --category standards --id IPC-2221B \\
        --year 2021 --config knowledge-sources.json

Exit codes:
    0: 更新成功
    1: 更新失败
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


def save_config(config_path: Path, data: Dict[str, Any]):
    """保存配置文件"""
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误: 保存文件失败: {e}", file=sys.stderr)
        sys.exit(1)


def update_entry(entry: Dict[str, Any], args, category: str) -> Dict[str, str]:
    """
    更新条目字段

    Returns:
        更新字段的映射 {field_name: old_value -> new_value}
    """
    changes = {}

    # 通用字段
    if args.enabled is not None:
        old_value = entry.get("enabled", False)
        entry["enabled"] = args.enabled
        if old_value != args.enabled:
            changes["enabled"] = f"{old_value} -> {args.enabled}"

    if args.location:
        old_value = entry.get("location", "")
        entry["location"] = args.location
        if old_value != args.location:
            changes["location"] = "已更新"

    # standards 类别字段
    if category == "standards":
        if args.standard_number:
            old_value = entry.get("standard_number", "")
            entry["standard_number"] = args.standard_number
            if old_value != args.standard_number:
                changes["standard_number"] = f"{old_value} -> {args.standard_number}"

        if args.year:
            old_value = entry.get("year", 0)
            entry["year"] = int(args.year)
            if old_value != int(args.year):
                changes["year"] = f"{old_value} -> {args.year}"

        if args.deprecated is not None:
            old_value = entry.get("deprecated", False)
            entry["deprecated"] = args.deprecated
            if old_value != args.deprecated:
                changes["deprecated"] = f"{old_value} -> {args.deprecated}"

        if args.title:
            entry["title"] = args.title
            changes["title"] = "已更新"

        if args.abstract:
            entry["abstract"] = args.abstract
            changes["abstract"] = "已更新"

    # company_kb 类别字段
    elif category == "company_kb":
        if args.type:
            old_value = entry.get("type", "")
            entry["type"] = args.type
            if old_value != args.type:
                changes["type"] = f"{old_value} -> {args.type}"

        if args.title:
            entry["title"] = args.title
            changes["title"] = "已更新"

        if args.authors:
            authors = [a.strip() for a in args.authors.split(",")]
            entry["authors"] = authors
            changes["authors"] = f"已更新为 {len(authors)} 位作者"

        if args.year:
            old_value = entry.get("year", 0)
            entry["year"] = int(args.year)
            if old_value != int(args.year):
                changes["year"] = f"{old_value} -> {args.year}"

        if args.abstract:
            entry["abstract"] = args.abstract
            changes["abstract"] = "已更新"

    # reference_designs 类别字段
    elif category == "reference_designs":
        if args.name:
            old_value = entry.get("name", "")
            entry["name"] = args.name
            if old_value != args.name:
                changes["name"] = f"{old_value} -> {args.name}"

        if args.vendor:
            old_value = entry.get("vendor", "")
            entry["vendor"] = args.vendor
            if old_value != args.vendor:
                changes["vendor"] = f"{old_value} -> {args.vendor}"

        if args.url:
            entry["url"] = args.url
            changes["url"] = "已更新"

        if args.key_parameters:
            try:
                key_parameters = json.loads(args.key_parameters)
                entry["key_parameters"] = key_parameters
                changes["key_parameters"] = "已更新"
            except json.JSONDecodeError:
                print("警告: key_parameters 不是有效的 JSON，跳过更新", file=sys.stderr)

    # web 类别字段
    elif category == "web":
        if args.name:
            old_value = entry.get("name", "")
            entry["name"] = args.name
            if old_value != args.name:
                changes["name"] = f"{old_value} -> {args.name}"

        if args.url:
            entry["url"] = args.url
            changes["url"] = "已更新"

        if args.api_key:
            old_value = entry.get("api_key", "")
            entry["api_key"] = args.api_key
            # 不显示实际密钥
            if "{{PLACEHOLDER" in old_value and "ENV:" in args.api_key:
                changes["api_key"] = "占位符 -> ENV 引用"
            elif old_value != args.api_key:
                changes["api_key"] = "已更新"

        if args.method:
            old_value = entry.get("method", "")
            entry["method"] = args.method
            if old_value != args.method:
                changes["method"] = f"{old_value} -> {args.method}"

        if args.headers:
            try:
                headers = json.loads(args.headers)
                entry["headers"] = headers
                changes["headers"] = "已更新"
            except json.JSONDecodeError:
                print("警告: headers 不是有效的 JSON，跳过更新", file=sys.stderr)

        if args.body_template:
            try:
                body_template = json.loads(args.body_template)
                entry["body_template"] = body_template
                changes["body_template"] = "已更新"
            except json.JSONDecodeError:
                print("警告: body_template 不是有效的 JSON，跳过更新", file=sys.stderr)

        if args.response_parser:
            try:
                response_parser = json.loads(args.response_parser)
                entry["response_parser"] = response_parser
                changes["response_parser"] = "已更新"
            except json.JSONDecodeError:
                print("警告: response_parser 不是有效的 JSON，跳过更新", file=sys.stderr)

    return changes


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="更新知识源条目字段", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 通用参数
    parser.add_argument("--category", required=True, choices=VALID_CATEGORIES, help="知识源类别")
    parser.add_argument("--id", required=True, help="条目唯一标识符")
    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument(
        "--enabled", type=lambda x: x.lower() in ("true", "1", "yes"), help="是否启用 (true/false)"
    )
    parser.add_argument("--location", help="文件路径或 URL")

    # standards 类别参数
    parser.add_argument("--standard_number", help="标准编号 (standards)")
    parser.add_argument("--year", help="发布年份 (standards, company_kb)")
    parser.add_argument(
        "--deprecated",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        help="是否已废弃 (standards)",
    )
    parser.add_argument("--title", help="标题 (standards, company_kb)")
    parser.add_argument("--abstract", help="摘要 (standards, company_kb)")

    # company_kb 类别参数
    parser.add_argument("--type", help="文档类型 (company_kb)")
    parser.add_argument("--authors", help="作者列表，逗号分隔 (company_kb)")

    # reference_designs 类别参数
    parser.add_argument("--name", help="参考设计名称 (reference_designs, web)")
    parser.add_argument("--vendor", help="供应商 (reference_designs)")
    parser.add_argument("--url", help="官方链接 (reference_designs, web)")
    parser.add_argument("--key_parameters", help="关键参数 JSON 字符串 (reference_designs)")

    # web 类别参数
    parser.add_argument("--api_key", help="API 密钥 (web)")
    parser.add_argument("--method", help="HTTP 方法 (web)")
    parser.add_argument("--headers", help="请求头 JSON 字符串 (web)")
    parser.add_argument("--body_template", help="请求体模板 JSON 字符串 (web)")
    parser.add_argument("--response_parser", help="响应解析器 JSON 字符串 (web)")

    args = parser.parse_args()

    # 加载配置
    print(f"加载配置文件: {args.config}")
    data = load_config(args.config)

    # 检查类别是否存在
    if args.category not in data:
        print(f"错误: 类别 '{args.category}' 不存在", file=sys.stderr)
        sys.exit(1)

    if "sources" not in data[args.category]:
        print(f"错误: 类别 '{args.category}' 缺少 sources 字段", file=sys.stderr)
        sys.exit(1)

    # 查找条目
    sources = data[args.category]["sources"]
    entry = None
    for source in sources:
        if isinstance(source, dict) and source.get("id") == args.id:
            entry = source
            break

    if entry is None:
        print(f"错误: ID '{args.id}' 不存在于 {args.category} 类别", file=sys.stderr)
        sys.exit(1)

    # 更新条目
    try:
        changes = update_entry(entry, args, args.category)
    except Exception as e:
        print(f"错误: 更新条目失败: {e}", file=sys.stderr)
        sys.exit(1)

    if not changes:
        print("警告: 没有字段需要更新", file=sys.stderr)
        sys.exit(0)

    # 保存配置
    save_config(args.config, data)

    print(f"✓ 成功更新条目: [{args.category}] {args.id}")
    print("  更新字段:")
    for field, change in changes.items():
        print(f"    - {field}: {change}")


if __name__ == "__main__":
    main()
