#!/usr/bin/env python3
"""
skillconfig_list.py - 列出所有 Skills 及其配置状态

用法:
    python skillconfig_list.py [--config CONFIG_FILE] [--format {text|json}]

参数:
    --config: skill_config.json 文件路径 (可选,默认 .elecspecify/memory/skill_config.json)
    --format: 输出格式 text(默认) 或 json

输出:
    text 格式: 按分类显示 Skills,包含启用状态(✅/❌)和描述
    json 格式: 完整的 Skills 配置 JSON

退出码:
    0: 成功
    1: 配置文件不存在
    4: JSON 格式错误
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def find_config_file(config_path: str = None) -> Path:
    """
    查找 skill_config.json 文件

    Args:
        config_path: 指定的配置文件路径 (可选)

    Returns:
        配置文件的 Path 对象

    Raises:
        FileNotFoundError: 配置文件不存在
    """
    if config_path:
        config_file = Path(config_path)
    else:
        # 默认路径
        config_file = Path(".elecspecify/memory/skill_config.json")

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")

    return config_file


def load_config(config_file: Path) -> Dict[str, Any]:
    """
    加载 skill_config.json

    Args:
        config_file: 配置文件路径

    Returns:
        配置字典

    Raises:
        json.JSONDecodeError: JSON 格式错误
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"配置文件 JSON 格式错误: {str(e)}", e.doc, e.pos
        )


def format_text_output(config: Dict[str, Any]) -> str:
    """
    生成文本格式输出

    Args:
        config: skill_config.json 配置字典

    Returns:
        格式化的文本输出
    """
    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append(f"ElecSpeckit Skills 列表 (v{config.get('version', 'unknown')})")
    output_lines.append(f"平台: {config.get('platform', 'unknown')}")
    output_lines.append("=" * 60)
    output_lines.append("")

    skills = config.get("skills", {})

    # 分类名称映射 (中文显示)
    category_names = {
        "information_retrieval": "信息检索类",
        "document_generation": "文档生成与可视化类",
        "data_analysis": "数据分析类",
        "embedded_systems": "嵌入式系统类",
        "component_search": "元器件采购类",
        "domain_analysis": "领域分析类",
        "meta": "元 Skill",
    }

    for category, category_skills in skills.items():
        category_display = category_names.get(category, category)
        output_lines.append(f"## {category_display} ({category})")
        output_lines.append("")

        for skill_name, skill_data in category_skills.items():
            enabled = skill_data.get("enabled", False)
            requires_api = skill_data.get("requires_api", False)
            description = skill_data.get("description", "无描述")

            # 状态图标
            status_icon = "✅" if enabled else "❌"

            # API 要求标记
            api_mark = " [需要 API]" if requires_api else ""

            output_lines.append(f"{status_icon} **{skill_name}**{api_mark}")
            output_lines.append(f"   {description}")
            output_lines.append("")

    output_lines.append("=" * 60)
    output_lines.append("图例: ✅ 已启用 | ❌ 已禁用 | [需要 API] 需要配置 API 密钥")
    output_lines.append("")

    return "\n".join(output_lines)


def format_json_output(config: Dict[str, Any]) -> str:
    """
    生成 JSON 格式输出

    Args:
        config: skill_config.json 配置字典

    Returns:
        JSON 字符串
    """
    return json.dumps(config, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="列出所有 ElecSpeckit Skills 及其配置状态"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="skill_config.json 文件路径 (默认: .elecspecify/memory/skill_config.json)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="输出格式: text(默认) 或 json",
    )

    args = parser.parse_args()

    try:
        # 查找并加载配置文件
        config_file = find_config_file(args.config)
        config = load_config(config_file)

        # 生成输出
        if args.format == "json":
            output = format_json_output(config)
        else:
            output = format_text_output(config)

        print(output)
        return 0

    except FileNotFoundError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件 JSON 格式错误\n{str(e)}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
