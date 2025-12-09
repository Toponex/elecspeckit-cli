#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kbconfig_delete.py - 删除知识源条目

支持安全删除条目 (per FR-017, T054e):
- 删除指定 ID 的条目
- 确认删除前显示条目信息
- 支持强制删除模式（跳过确认）

Usage:
    # 删除标准条目
    python kbconfig_delete.py --category standards --id IPC-2221B \
        --config .elecspecify/memory/knowledge-sources.json

    # 强制删除（跳过确认）
    python kbconfig_delete.py --category standards --id IPC-2221B \
        --config knowledge-sources.json --force

Exit codes:
    0: 删除成功
    1: 删除失败
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


def format_entry_info(entry: Dict[str, Any], category: str) -> str:
    """格式化条目信息用于确认"""
    lines = []
    entry_id = entry.get("id", "unknown")
    enabled = entry.get("enabled", False)

    lines.append(f"ID: {entry_id}")
    lines.append(f"启用状态: {'已启用' if enabled else '已禁用'}")

    if category == "standards":
        lines.append(f"标准编号: {entry.get('standard_number', '')}")
        lines.append(f"年份: {entry.get('year', '')}")
        lines.append(f"标题: {entry.get('title', '')}")
        if entry.get("deprecated", False):
            lines.append("状态: 已废弃")

    elif category == "company_kb":
        lines.append(f"标题: {entry.get('title', '')}")
        lines.append(f"类型: {entry.get('type', '')}")
        lines.append(f"年份: {entry.get('year', '')}")
        authors = entry.get("authors", [])
        if authors:
            lines.append(f"作者: {', '.join(authors)}")

    elif category == "reference_designs":
        lines.append(f"名称: {entry.get('name', '')}")
        lines.append(f"供应商: {entry.get('vendor', '')}")
        lines.append(f"URL: {entry.get('url', '')}")

    elif category == "web":
        lines.append(f"名称: {entry.get('name', '')}")
        lines.append(f"URL: {entry.get('url', '')}")
        api_key = entry.get("api_key", "")
        if api_key:
            if "{{PLACEHOLDER" in api_key:
                lines.append("API密钥: 占位符")
            elif api_key.startswith("ENV:"):
                lines.append(f"API密钥: {api_key}")
            else:
                lines.append("API密钥: 已配置")

    return "\n  ".join(lines)


def confirm_deletion(entry: Dict[str, Any], category: str) -> bool:
    """确认删除操作"""
    print()
    print("即将删除以下条目:")
    print()
    print(f"  {format_entry_info(entry, category)}")
    print()

    try:
        response = input("确认删除? (yes/no): ").strip().lower()
        return response in ["yes", "y", "是", "确认"]
    except (KeyboardInterrupt, EOFError):
        print("\n取消删除")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="删除知识源条目", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--category", required=True, choices=VALID_CATEGORIES, help="知识源类别")
    parser.add_argument("--id", required=True, help="条目唯一标识符")
    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument("--force", action="store_true", help="强制删除，跳过确认")

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
    entry_index = -1

    for idx, source in enumerate(sources):
        if isinstance(source, dict) and source.get("id") == args.id:
            entry = source
            entry_index = idx
            break

    if entry is None:
        print(f"错误: ID '{args.id}' 不存在于 {args.category} 类别", file=sys.stderr)
        sys.exit(1)

    # 确认删除（除非使用 --force）
    if not args.force:
        if not confirm_deletion(entry, args.category):
            print("删除已取消")
            sys.exit(0)

    # 删除条目
    try:
        del data[args.category]["sources"][entry_index]
    except Exception as e:
        print(f"错误: 删除条目失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 保存配置
    save_config(args.config, data)

    print(f"✓ 成功删除条目: [{args.category}] {args.id}")
    print(f"  当前 {args.category} 类别共有 {len(data[args.category]['sources'])} 个条目")


if __name__ == "__main__":
    main()
