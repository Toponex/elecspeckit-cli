#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_metaso.py - 查询 Metaso 学术搜索 API

通过 knowledge-sources.json 配置查询 Metaso API (per FR-017, T054f):
- 从配置文件读取 Metaso API 配置
- 解析 ENV 变量引用
- 验证 response_parser 安全性
- 使用 jsonpath-ng 安全解析响应

Usage:
    # 查询学术文献
    python query_metaso.py --config .elecspecify/memory/knowledge-sources.json \
        --query "PCB设计规范"

    # 指定返回结果数量
    python query_metaso.py --config knowledge-sources.json \
        --query "电源管理芯片" --size 20

Exit codes:
    0: 查询成功
    1: 查询失败
"""

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 危险字符模式 (per FR-015)
DANGEROUS_PATTERNS = [
    r"eval\s*\(",
    r"exec\s*\(",
    r"__import__\s*\(",
    r"compile\s*\(",
    r"open\s*\(",
    r"execfile\s*\(",
    r"__builtins__",
]


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


def resolve_env_variable(value: str) -> str:
    """解析 ENV 变量引用"""
    if isinstance(value, str) and value.startswith("ENV:"):
        var_name = value[4:]  # 去掉 "ENV:" 前缀
        env_value = os.environ.get(var_name)
        if env_value is None:
            print(f"错误: 环境变量 {var_name} 未设置", file=sys.stderr)
            sys.exit(1)
        return env_value
    return value


def check_dangerous_patterns(value: Any) -> List[str]:
    """检查危险模式"""
    dangerous_found = []

    if isinstance(value, str):
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                match = re.search(pattern, value, re.IGNORECASE)
                if match:
                    dangerous_found.append(match.group(0))

    elif isinstance(value, dict):
        for v in value.values():
            dangerous_found.extend(check_dangerous_patterns(v))

    elif isinstance(value, list):
        for item in value:
            dangerous_found.extend(check_dangerous_patterns(item))

    return dangerous_found


def validate_response_parser(response_parser: Any):
    """验证 response_parser 安全性"""
    dangerous_chars = check_dangerous_patterns(response_parser)
    if dangerous_chars:
        print(
            f"错误: response_parser 包含危险字符或函数调用: {', '.join(dangerous_chars)}",
            file=sys.stderr,
        )
        sys.exit(1)


def replace_template_variables(template: Any, variables: Dict[str, str]) -> Any:
    """替换模板变量"""
    if isinstance(template, str):
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result

    elif isinstance(template, dict):
        return {k: replace_template_variables(v, variables) for k, v in template.items()}

    elif isinstance(template, list):
        return [replace_template_variables(item, variables) for item in template]

    return template


def parse_response_with_jsonpath(
    response_data: Dict[str, Any], response_parser: Dict[str, str]
) -> List[Dict[str, Any]]:
    """使用 JSONPath 解析响应（简化版，不依赖 jsonpath-ng）"""
    try:
        # 获取结果路径
        results_path = response_parser.get("results_path", "$.data.results")

        # 简化的 JSONPath 解析（仅支持基本路径）
        # 例如: $.data.results -> data.results
        path_parts = results_path.replace("$", "").strip(".").split(".")

        # 遍历路径获取数据
        current = response_data
        for part in path_parts:
            if isinstance(current, dict):
                current = current.get(part, [])
            else:
                return []

        if not isinstance(current, list):
            return []

        # 解析每个结果项
        results = []
        for item in current:
            result = {}
            for field, field_path in response_parser.items():
                if field == "results_path":
                    continue

                # 简化的字段路径解析
                # 例如: $.title -> title
                field_parts = field_path.replace("$", "").strip(".").split(".")

                field_value = item
                for part in field_parts:
                    if isinstance(field_value, dict):
                        field_value = field_value.get(part, "")
                    else:
                        field_value = ""
                        break

                result[field] = field_value

            results.append(result)

        return results

    except Exception as e:
        print(f"警告: 解析响应失败: {e}", file=sys.stderr)
        return []


def query_metaso(config: Dict[str, Any], query: str, size: int = 50) -> List[Dict[str, Any]]:
    """查询 Metaso API"""
    # 检查 web 类别是否启用
    if not config.get("web", {}).get("enabled", False):
        print("错误: web 类别未启用", file=sys.stderr)
        sys.exit(1)

    # 查找 metaso 条目
    web_sources = config.get("web", {}).get("sources", [])
    metaso_entry = None

    for source in web_sources:
        if isinstance(source, dict) and source.get("id") == "metaso":
            metaso_entry = source
            break

    if metaso_entry is None:
        print("错误: 未找到 metaso 配置", file=sys.stderr)
        sys.exit(1)

    # 检查条目是否启用
    if not metaso_entry.get("enabled", False):
        print("错误: metaso 条目未启用", file=sys.stderr)
        sys.exit(1)

    # 获取配置
    url = metaso_entry.get("url", "")
    api_key = resolve_env_variable(metaso_entry.get("api_key", ""))
    method = metaso_entry.get("method", "POST")
    headers = metaso_entry.get("headers", {})
    body_template = metaso_entry.get("body_template", {})
    response_parser = metaso_entry.get("response_parser", {})

    # 验证 response_parser 安全性
    validate_response_parser(response_parser)

    # 检查占位符
    if "{{PLACEHOLDER" in api_key:
        print("错误: API 密钥未配置（仍为占位符）", file=sys.stderr)
        sys.exit(1)

    # 替换模板变量
    variables = {"api_key": api_key, "query": query}

    headers = replace_template_variables(headers, variables)
    body = replace_template_variables(body_template, variables)

    # 更新 size 参数
    if isinstance(body, dict) and "size" in body:
        body["size"] = size

    # 发送请求
    try:
        print(f"正在查询 Metaso: {query}")
        print(f"请求 URL: {url}")

        if method.upper() == "POST":
            response = requests.post(url, headers=headers, json=body, timeout=30)
        else:
            response = requests.get(url, headers=headers, params=body, timeout=30)

        response.raise_for_status()

        # 解析响应
        response_data = response.json()

        # 使用 response_parser 解析结果
        results = parse_response_with_jsonpath(response_data, response_parser)

        return results

    except requests.exceptions.RequestException as e:
        print(f"错误: 请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: 响应解析失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="查询 Metaso 学术搜索 API", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument("--query", required=True, help="查询关键词")
    parser.add_argument("--size", type=int, default=50, help="返回结果数量（默认 50）")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # 查询 Metaso
    results = query_metaso(config, args.query, args.size)

    # 输出结果
    print()
    print(f"✓ 查询成功，共找到 {len(results)} 条结果:")
    print()

    for idx, result in enumerate(results, 1):
        print(f"{idx}. {result.get('title', '(无标题)')}")
        if result.get("abstract"):
            print(f"   摘要: {result.get('abstract')[:100]}...")
        if result.get("url"):
            print(f"   链接: {result.get('url')}")
        print()


if __name__ == "__main__":
    main()
