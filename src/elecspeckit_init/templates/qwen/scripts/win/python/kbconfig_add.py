#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kbconfig_add.py - 添加知识源条目到 knowledge-sources.json

支持四大类别 (per FR-017, T054b):
- standards: 行业/企业标准
- company_kb: 公司知识库
- reference_designs: 参考设计
- web: 外部 API 知识源

Usage:
    # 添加标准
    python kbconfig_add.py --category standards --id IPC-2221B --standard_number IPC-2221B \\
        --year 2018 --title "PCB设计通用标准" --location "F:\\standards\\ipc2221b.pdf" \\
        --config .elecspecify/memory/knowledge-sources.json

    # 添加参考设计
    python kbconfig_add.py --category reference_designs --id TI-PMP22682 \\
        --name "TI 65W PD充电器" --vendor TI --url "https://www.ti.com/tool/PMP22682" \\
        --location "F:\\ref_designs\\TI-PMP22682" --config knowledge-sources.json

Exit codes:
    0: 添加成功
    1: 添加失败
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


def add_standards_entry(args) -> Dict[str, Any]:
    """创建 standards 类别条目"""
    entry = {
        "id": args.id,
        "standard_number": args.standard_number,
        "year": int(args.year),
        "deprecated": args.deprecated if args.deprecated is not None else False,
        "title": args.title,
        "abstract": args.abstract or "",
        "location": args.location,
        "enabled": args.enabled if args.enabled is not None else True,
    }
    return entry


def add_company_kb_entry(args) -> Dict[str, Any]:
    """创建 company_kb 类别条目"""
    # authors 参数可以是逗号分隔的字符串
    authors = []
    if args.authors:
        authors = [a.strip() for a in args.authors.split(",")]

    entry = {
        "id": args.id,
        "type": args.type or "document",
        "title": args.title,
        "authors": authors,
        "year": int(args.year) if args.year else 2024,
        "abstract": args.abstract or "",
        "location": args.location,
        "enabled": args.enabled if args.enabled is not None else True,
    }
    return entry


def add_reference_design_entry(args) -> Dict[str, Any]:
    """创建 reference_designs 类别条目"""
    # key_parameters 可以是 JSON 字符串或空对象
    key_parameters = {}
    if args.key_parameters:
        try:
            key_parameters = json.loads(args.key_parameters)
        except json.JSONDecodeError:
            print("警告: key_parameters 不是有效的 JSON，使用空对象", file=sys.stderr)

    entry = {
        "id": args.id,
        "name": args.name,
        "vendor": args.vendor or "",
        "url": args.url or "",
        "key_parameters": key_parameters,
        "location": args.location or "",
        "enabled": args.enabled if args.enabled is not None else True,
    }
    return entry


def add_web_entry(args) -> Dict[str, Any]:
    """创建 web 类别条目"""
    # headers 和 body_template 可以是 JSON 字符串
    headers = {}
    if args.headers:
        try:
            headers = json.loads(args.headers)
        except json.JSONDecodeError:
            print("警告: headers 不是有效的 JSON，使用空对象", file=sys.stderr)

    body_template = {}
    if args.body_template:
        try:
            body_template = json.loads(args.body_template)
        except json.JSONDecodeError:
            print("警告: body_template 不是有效的 JSON，使用空对象", file=sys.stderr)

    response_parser = {}
    if args.response_parser:
        try:
            response_parser = json.loads(args.response_parser)
        except json.JSONDecodeError:
            print("警告: response_parser 不是有效的 JSON，使用空对象", file=sys.stderr)

    entry = {
        "id": args.id,
        "name": args.name,
        "url": args.url,
        "api_key": args.api_key or "{{PLACEHOLDER:请填写API密钥}}",
        "method": args.method or "POST",
        "headers": headers,
        "body_template": body_template,
        "response_parser": response_parser,
        "enabled": args.enabled if args.enabled is not None else False,
    }
    return entry


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="添加知识源条目到 knowledge-sources.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 通用参数
    parser.add_argument("--category", required=True, choices=VALID_CATEGORIES, help="知识源类别")
    parser.add_argument("--id", required=True, help="条目唯一标识符")
    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument(
        "--enabled", type=lambda x: x.lower() in ("true", "1", "yes"), help="是否启用 (true/false)"
    )

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
    parser.add_argument(
        "--location", help="文件路径或 URL (standards, company_kb, reference_designs)"
    )

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

    # 检查 ID 是否已存在
    sources = data[args.category]["sources"]
    for source in sources:
        if isinstance(source, dict) and source.get("id") == args.id:
            print(f"错误: ID '{args.id}' 已存在于 {args.category} 类别", file=sys.stderr)
            sys.exit(1)

    # 根据类别创建条目
    try:
        if args.category == "standards":
            entry = add_standards_entry(args)
        elif args.category == "company_kb":
            entry = add_company_kb_entry(args)
        elif args.category == "reference_designs":
            entry = add_reference_design_entry(args)
        elif args.category == "web":
            entry = add_web_entry(args)
        else:
            print(f"错误: 不支持的类别: {args.category}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"错误: 创建条目失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 添加到 sources 数组
    data[args.category]["sources"].append(entry)

    # 保存配置
    save_config(args.config, data)

    print(f"✓ 成功添加条目: [{args.category}] {args.id}")
    print(f"  当前 {args.category} 类别共有 {len(data[args.category]['sources'])} 个条目")


if __name__ == "__main__":
    main()
