#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_volces.py - 查询 Volces 知识库 API

通过 knowledge-sources.json 配置查询 Volces API (per FR-017, T054g):
- 从配置文件读取 Volces API 配置
- 解析 ENV 变量引用
- 验证 response_parser 安全性
- 使用 DeepSeek 模型进行知识查询

Usage:
    # 查询技术问题
    python query_volces.py --config .elecspecify/memory/knowledge-sources.json \
        --query "如何设计高效的电源管理电路？"

    # 指定系统提示词
    python query_volces.py --config knowledge-sources.json \
        --query "PCB布线规则" --system "你是电子工程专家"

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
    """使用 JSONPath 解析响应（简化版）"""
    try:
        # 获取结果路径
        results_path = response_parser.get("results_path", "$.choices")

        # 简化的 JSONPath 解析
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


def query_volces(
    config: Dict[str, Any], query: str, system_prompt: str = None
) -> List[Dict[str, Any]]:
    """查询 Volces API"""
    # 检查 web 类别是否启用
    if not config.get("web", {}).get("enabled", False):
        print("错误: web 类别未启用", file=sys.stderr)
        sys.exit(1)

    # 查找 volces 条目
    web_sources = config.get("web", {}).get("sources", [])
    volces_entry = None

    for source in web_sources:
        if isinstance(source, dict) and source.get("id") == "volces":
            volces_entry = source
            break

    if volces_entry is None:
        print("错误: 未找到 volces 配置", file=sys.stderr)
        sys.exit(1)

    # 检查条目是否启用
    if not volces_entry.get("enabled", False):
        print("错误: volces 条目未启用", file=sys.stderr)
        sys.exit(1)

    # 获取配置
    url = volces_entry.get("url", "")
    api_key = resolve_env_variable(volces_entry.get("api_key", ""))
    method = volces_entry.get("method", "POST")
    headers = volces_entry.get("headers", {})
    body_template = volces_entry.get("body_template", {})
    response_parser = volces_entry.get("response_parser", {})

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

    # 更新系统提示词（如果提供）
    if system_prompt and isinstance(body, dict) and "messages" in body:
        for message in body["messages"]:
            if message.get("role") == "system":
                message["content"] = system_prompt
                break

    # 发送请求
    try:
        print(f"正在查询 Volces: {query}")
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
        description="查询 Volces 知识库 API", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--config", required=True, type=Path, help="配置文件路径")
    parser.add_argument("--query", required=True, help="查询问题")
    parser.add_argument("--system", default=None, help="系统提示词（可选）")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # 查询 Volces
    results = query_volces(config, args.query, args.system)

    # 输出结果
    print()
    print(f"✓ 查询成功，共收到 {len(results)} 条回复:")
    print()

    for idx, result in enumerate(results, 1):
        content = result.get("content", "(无内容)")
        print(f"回复 {idx}:")
        print(content)
        print()


if __name__ == "__main__":
    main()
