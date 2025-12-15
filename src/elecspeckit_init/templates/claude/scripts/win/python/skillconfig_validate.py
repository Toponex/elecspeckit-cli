#!/usr/bin/env python3
"""
skillconfig_validate.py - 验证 skill_config.json 与实际 Skills 文件一致性

功能:
- 验证配置文件与 Skills 目录一致性
- 检查 enabled 状态与文件名匹配
- 检查配置中的 Skill 目录是否存在
- 检查 Skills 目录中的 Skill 是否在配置中

用法:
    python skillconfig_validate.py [--config CONFIG_FILE] [--skills-dir SKILLS_DIR]

参数:
    --config: skill_config.json 文件路径 (可选,默认 .elecspecify/memory/skill_config.json)
    --skills-dir: Skills 目录路径 (可选,默认 .claude/skills/)

输出:
    JSON 格式验证结果:
    {
      "status": "valid" | "invalid",
      "errors": [{"skill": "skill-name", "error": "错误描述"}],
      "warnings": [{"skill": "skill-name", "warning": "警告描述"}]
    }

退出码:
    0: 验证通过 (status: "valid")
    1: 配置文件不存在
    3: 验证失败 (status: "invalid")
    4: JSON 格式错误
    5: 其他错误
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def find_config_file(config_path: str = None) -> Path:
    """查找 skill_config.json 文件"""
    if config_path:
        config_file = Path(config_path)
    else:
        config_file = Path(".elecspecify/memory/skill_config.json")

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")

    return config_file


def load_config(config_file: Path) -> Dict[str, Any]:
    """加载 skill_config.json"""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"配置文件 JSON 格式错误: {str(e)}", e.doc, e.pos
        )


def validate_skill_files(
    config: Dict[str, Any], skills_dir: Path
) -> tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    验证 Skills 文件与配置一致性

    Returns:
        (errors, warnings) 列表
    """
    errors = []
    warnings = []

    # 检查 Skills 目录是否存在
    if not skills_dir.exists():
        errors.append(
            {
                "skill": "skills_directory",
                "error": f"Skills 目录不存在: {skills_dir}",
            }
        )
        return errors, warnings

    # 获取配置中的所有 Skills
    config_skills = {}
    for category, category_skills in config.get("skills", {}).items():
        for skill_name, skill_data in category_skills.items():
            config_skills[skill_name] = skill_data

    # 1. 验证配置中的 Skills 目录和文件
    for skill_name, skill_data in config_skills.items():
        skill_dir = skills_dir / skill_name

        # 检查目录是否存在
        if not skill_dir.exists():
            errors.append(
                {
                    "skill": skill_name,
                    "error": f"Skill 目录不存在: {skill_dir}",
                }
            )
            continue

        # 检查文件名与 enabled 状态匹配
        enabled = skill_data.get("enabled", False)
        active_file = skill_dir / "SKILL.md"
        disabled_file = skill_dir / "(DISABLED)SKILL.md"

        if enabled:
            # 应该是 SKILL.md
            if not active_file.exists():
                if disabled_file.exists():
                    errors.append(
                        {
                            "skill": skill_name,
                            "error": f"enabled: true 但文件名为 (DISABLED)SKILL.md",
                        }
                    )
                else:
                    errors.append(
                        {
                            "skill": skill_name,
                            "error": f"enabled: true 但 SKILL.md 文件不存在",
                        }
                    )
        else:
            # 应该是 (DISABLED)SKILL.md
            if not disabled_file.exists():
                if active_file.exists():
                    errors.append(
                        {
                            "skill": skill_name,
                            "error": f"enabled: false 但文件名为 SKILL.md",
                        }
                    )
                else:
                    errors.append(
                        {
                            "skill": skill_name,
                            "error": f"enabled: false 但 (DISABLED)SKILL.md 文件不存在",
                        }
                    )

    # 2. 检查 Skills 目录中的 Skill 是否在配置中
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name

        # 跳过隐藏目录和特殊目录
        if skill_name.startswith(".") or skill_name.startswith("_"):
            continue

        if skill_name not in config_skills:
            warnings.append(
                {
                    "skill": skill_name,
                    "warning": f"Skills 目录中存在但未在配置中: {skill_dir}",
                }
            )

    return errors, warnings


def validate_config(config_path: str = None, skills_dir: str = None) -> int:
    """
    验证配置

    Returns:
        退出码
    """
    try:
        # 加载配置
        config_file = find_config_file(config_path)
        config = load_config(config_file)

        # Skills 目录
        if skills_dir:
            skills_path = Path(skills_dir)
        else:
            skills_path = Path(".claude/skills")

        # 验证
        errors, warnings = validate_skill_files(config, skills_path)

        # 生成结果
        result = {
            "status": "valid" if len(errors) == 0 else "invalid",
            "errors": errors,
            "warnings": warnings,
        }

        # 输出 JSON 结果
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 返回退出码
        if len(errors) > 0:
            return 3  # 验证失败
        else:
            return 0  # 验证通过

    except FileNotFoundError as e:
        result = {
            "status": "invalid",
            "errors": [{"skill": "config", "error": str(e)}],
            "warnings": [],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    except json.JSONDecodeError as e:
        result = {
            "status": "invalid",
            "errors": [{"skill": "config", "error": f"JSON 格式错误: {str(e)}"}],
            "warnings": [],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 4
    except Exception as e:
        result = {
            "status": "invalid",
            "errors": [{"skill": "unknown", "error": str(e)}],
            "warnings": [],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 5


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="验证 skill_config.json 与 Skills 文件一致性")
    parser.add_argument(
        "--config",
        type=str,
        help="skill_config.json 文件路径 (默认: .elecspecify/memory/skill_config.json)",
    )
    parser.add_argument(
        "--skills-dir", type=str, help="Skills 目录路径 (默认: .claude/skills/)"
    )

    args = parser.parse_args()

    return validate_config(args.config, args.skills_dir)


if __name__ == "__main__":
    sys.exit(main())
