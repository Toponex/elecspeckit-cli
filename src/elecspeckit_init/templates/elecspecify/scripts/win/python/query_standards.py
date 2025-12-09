#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_standards.py - 查询本地标准文档

从 knowledge-sources.json 的 standards 类别查询本地标准文件:
- 支持标准编号搜索
- 支持标题关键词搜索
- 支持年份过滤
- 自动跳过已废弃的标准

Usage:
    # 查询特定标准
    python query_standards.py --config .elecspecify/memory/knowledge-sources.json \
        --query "IPC-2221B"

    # 关键词搜索
    python query_standards.py --config knowledge-sources.json \
        --query "PCB设计" --limit 10

    # 显示所有可用标准
    python query_standards.py --config knowledge-sources.json --list

Exit codes:
    0: 查询成功
    1: 查询失败或配置错误
"""

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


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


def query_standards(
    config: Dict[str, Any],
    query: str = None,
    limit: int = 10,
    list_all: bool = False,
    include_deprecated: bool = False,
) -> List[Dict[str, Any]]:
    """
    查询标准文档

    Args:
        config: 配置字典
        query: 查询字符串 (标准编号或关键词)
        limit: 返回结果数量限制
        list_all: 是否列出所有标准
        include_deprecated: 是否包含已废弃的标准

    Returns:
        匹配的标准列表
    """
    if "standards" not in config:
        print("错误: 配置文件缺少 standards 类别", file=sys.stderr)
        sys.exit(1)

    standards_config = config["standards"]

    # 检查是否启用
    if not standards_config.get("enabled", False):
        print("提示: standards 类别未启用 (enabled=false)", file=sys.stderr)
        return []

    sources = standards_config.get("sources", [])

    if not sources:
        print("提示: standards 类别无可用条目", file=sys.stderr)
        return []

    results = []

    for source in sources:
        # 跳过未启用的标准
        if not source.get("enabled", True):
            continue

        # 跳过已废弃的标准 (除非明确要求)
        if not include_deprecated and source.get("deprecated", False):
            continue

        # 如果是列出所有标准，直接添加
        if list_all:
            results.append(source)
            continue

        # 如果没有查询字符串，跳过
        if not query:
            continue

        # 搜索标准编号
        standard_number = source.get("standard_number", "").lower()
        if query.lower() in standard_number:
            results.append(source)
            continue

        # 搜索标题
        title = source.get("title", "").lower()
        if query.lower() in title:
            results.append(source)
            continue

        # 搜索摘要
        abstract = source.get("abstract", "").lower()
        if query.lower() in abstract:
            results.append(source)
            continue

    # 限制返回数量
    return results[:limit]


def format_standard(standard: Dict[str, Any]) -> str:
    """格式化标准信息"""
    lines = []
    lines.append(f"标准编号: {standard.get('standard_number', 'N/A')}")
    lines.append(f"标题: {standard.get('title', 'N/A')}")
    lines.append(f"年份: {standard.get('year', 'N/A')}")

    if standard.get("deprecated", False):
        lines.append("状态: 已废弃 ⚠️")
    else:
        lines.append("状态: 有效 ✓")

    abstract = standard.get("abstract", "")
    if abstract:
        lines.append(f"摘要: {abstract}")

    location = standard.get("location", "")
    if location:
        lines.append(f"位置: {location}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="查询本地标准文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--config", type=Path, required=True, help="knowledge-sources.json 配置文件路径"
    )

    parser.add_argument("--query", type=str, help="查询字符串 (标准编号或关键词)")

    parser.add_argument("--limit", type=int, default=10, help="返回结果数量限制 (默认: 10)")

    parser.add_argument("--list", action="store_true", dest="list_all", help="列出所有可用标准")

    parser.add_argument("--include-deprecated", action="store_true", help="包含已废弃的标准")

    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # 执行查询
    results = query_standards(
        config,
        query=args.query,
        limit=args.limit,
        list_all=args.list_all,
        include_deprecated=args.include_deprecated,
    )

    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("未找到匹配的标准")
        else:
            print(f"找到 {len(results)} 个标准:\n")
            for i, standard in enumerate(results, 1):
                print(f"[{i}]")
                print(format_standard(standard))
                print()


if __name__ == "__main__":
    main()
