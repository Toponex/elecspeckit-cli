#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_reference_design.py - 查询本地参考设计文档

从 knowledge-sources.json 的 reference_designs 类别查询参考设计:
- 支持名称搜索
- 支持供应商过滤
- 支持关键参数搜索
- 显示本地文件路径

Usage:
    # 查询特定供应商的参考设计
    python query_reference_design.py --config .elecspecify/memory/knowledge-sources.json \
        --vendor "TI"

    # 关键词搜索
    python query_reference_design.py --config knowledge-sources.json \
        --query "电源" --limit 10

    # 显示所有参考设计
    python query_reference_design.py --config knowledge-sources.json --list

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


def query_reference_designs(
    config: Dict[str, Any],
    query: str = None,
    vendor: str = None,
    limit: int = 10,
    list_all: bool = False,
) -> List[Dict[str, Any]]:
    """
    查询参考设计

    Args:
        config: 配置字典
        query: 查询字符串 (名称或参数关键词)
        vendor: 供应商过滤
        limit: 返回结果数量限制
        list_all: 是否列出所有参考设计

    Returns:
        匹配的参考设计列表
    """
    if "reference_designs" not in config:
        print("错误: 配置文件缺少 reference_designs 类别", file=sys.stderr)
        sys.exit(1)

    ref_designs_config = config["reference_designs"]

    # 检查是否启用
    if not ref_designs_config.get("enabled", False):
        print("提示: reference_designs 类别未启用 (enabled=false)", file=sys.stderr)
        return []

    sources = ref_designs_config.get("sources", [])

    if not sources:
        print("提示: reference_designs 类别无可用条目", file=sys.stderr)
        return []

    results = []

    for source in sources:
        # 跳过未启用的参考设计
        if not source.get("enabled", True):
            continue

        # 如果是列出所有参考设计，直接添加
        if list_all:
            results.append(source)
            continue

        # 供应商过滤
        if vendor:
            source_vendor = source.get("vendor", "").lower()
            if vendor.lower() not in source_vendor:
                continue

        # 如果有供应商过滤但没有查询字符串，添加结果
        if vendor and not query:
            results.append(source)
            continue

        # 如果没有查询字符串，跳过
        if not query:
            continue

        # 搜索名称
        name = source.get("name", "").lower()
        if query.lower() in name:
            results.append(source)
            continue

        # 搜索关键参数
        key_parameters = source.get("key_parameters", {})
        if isinstance(key_parameters, dict):
            # 搜索参数键和值
            for key, value in key_parameters.items():
                if query.lower() in key.lower() or query.lower() in str(value).lower():
                    results.append(source)
                    break

    # 限制返回数量
    return results[:limit]


def format_reference_design(ref_design: Dict[str, Any]) -> str:
    """格式化参考设计信息"""
    lines = []
    lines.append(f"名称: {ref_design.get('name', 'N/A')}")
    lines.append(f"供应商: {ref_design.get('vendor', 'N/A')}")

    url = ref_design.get("url", "")
    if url:
        lines.append(f"官方链接: {url}")

    key_parameters = ref_design.get("key_parameters", {})
    if key_parameters:
        lines.append("关键参数:")
        for key, value in key_parameters.items():
            lines.append(f"  - {key}: {value}")

    location = ref_design.get("location", "")
    if location:
        lines.append(f"本地文件: {location}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="查询本地参考设计文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--config", type=Path, required=True, help="knowledge-sources.json 配置文件路径"
    )

    parser.add_argument("--query", type=str, help="查询字符串 (名称或参数关键词)")

    parser.add_argument("--vendor", type=str, help='供应商过滤 (如 "TI", "Analog Devices")')

    parser.add_argument("--limit", type=int, default=10, help="返回结果数量限制 (默认: 10)")

    parser.add_argument("--list", action="store_true", dest="list_all", help="列出所有可用参考设计")

    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # 执行查询
    results = query_reference_designs(
        config, query=args.query, vendor=args.vendor, limit=args.limit, list_all=args.list_all
    )

    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("未找到匹配的参考设计")
        else:
            print(f"找到 {len(results)} 个参考设计:\n")
            for i, ref_design in enumerate(results, 1):
                print(f"[{i}]")
                print(format_reference_design(ref_design))
                print()


if __name__ == "__main__":
    main()
