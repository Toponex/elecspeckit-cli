#!/usr/bin/env python3
"""
skillconfig_list.py - 列出所有 Skills 及其配置状态

用法:
    python skillconfig_list.py [--format {text|json}]

输出:
    text: 文本格式，按分类显示，带状态图标
    json: JSON 格式，完整配置数据

退出码:
    0: 成功
    1: 配置文件不存在
    4: JSON 格式错误
"""

import json
import sys
from pathlib import Path


def find_project_root():
    """从当前目录向上查找项目根目录（包含 .elecspecify/ 的目录）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".elecspecify").exists():
            return current
        current = current.parent
    return None


def load_skill_config():
    """加载项目的 skill_config.json"""
    project_root = find_project_root()
    if not project_root:
        print("错误: 未找到 ElecSpecKit 项目根目录（需要 .elecspecify/ 目录）", file=sys.stderr)
        print("提示: 请在项目目录中运行此命令", file=sys.stderr)
        sys.exit(1)

    config_file = project_root / ".elecspecify" / "memory" / "skill_config.json"

    if not config_file.exists():
        print(f"错误: 配置文件不存在: {config_file}", file=sys.stderr)
        print("提示: 请运行 'elecspeckit init' 初始化项目", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f), config_file
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件 JSON 格式错误: {e}", file=sys.stderr)
        sys.exit(4)


def format_text(config):
    """文本格式输出"""
    print("=" * 60)
    print(f"ElecSpecKit Skills 列表 (v{config.get('version', 'unknown')})")
    print(f"平台: {config.get('platform', 'unknown')}")
    print("=" * 60)
    print()

    category_names = {
        "information_retrieval": "信息检索类",
        "document_generation": "文档生成类",
        "data_analysis": "数据分析类",
        "embedded_systems": "嵌入式系统类",
        "component_search": "元器件采购类",
        "domain_analysis": "领域分析类",
        "meta": "元 Skill 类"
    }

    skills = config.get("skills", {})

    for category, category_name in category_names.items():
        if category not in skills:
            continue

        print(f"## {category_name} ({category})")
        print()

        for skill_name, skill_config in skills[category].items():
            enabled = skill_config.get("enabled", False)
            requires_api = skill_config.get("requires_api", False)
            has_api_key = bool(skill_config.get("api_key", "").strip())
            description = skill_config.get("description", "")

            # 状态图标
            if enabled:
                status = "✅"
            else:
                status = "❌"

            # API 密钥状态
            api_status = ""
            if requires_api:
                if has_api_key:
                    api_status = " [需要 API - 已配置]"
                else:
                    api_status = " [需要 API - 未配置]"

            print(f"{status} **{skill_name}**{api_status}")
            print(f"   {description}")
            print()

        print()

    print("=" * 60)
    print("图例: ✅ 已启用 | ❌ 已禁用")
    print()


def format_json(config):
    """JSON 格式输出"""
    print(json.dumps(config, indent=2, ensure_ascii=False))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="列出所有 ElecSpecKit Skills")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式 (默认: text)"
    )

    args = parser.parse_args()

    config, config_file = load_skill_config()

    if args.format == "text":
        format_text(config)
        print(f"配置文件: {config_file}")
    else:
        format_json(config)


if __name__ == "__main__":
    # 设置 UTF-8 输出（Windows 兼容性）
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    main()
