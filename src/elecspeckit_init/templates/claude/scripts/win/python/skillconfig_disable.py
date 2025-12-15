#!/usr/bin/env python3
"""
skillconfig_disable.py - 禁用指定的 Skill

功能:
- 更新 skill_config.json 中 enabled: false
- 重命名 SKILL.md → (DISABLED)SKILL.md
- 保留 API 密钥配置

用法:
    python skillconfig_disable.py <skill_name> [--config CONFIG_FILE] [--skills-dir SKILLS_DIR]

参数:
    skill_name: Skill 名称 (必需)
    --config: skill_config.json 文件路径 (可选,默认 .elecspecify/memory/skill_config.json)
    --skills-dir: Skills 目录路径 (可选,默认 .claude/skills/)

退出码:
    0: 成功
    1: 配置文件不存在或 Skill 不存在
    2: 文件重命名失败 (权限问题或文件被占用)
    4: JSON 格式错误
    5: 其他错误
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Tuple


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


def save_config(config_file: Path, config: Dict[str, Any]) -> None:
    """保存 skill_config.json"""
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def find_skill_in_config(config: Dict[str, Any], skill_name: str) -> Tuple[str, Dict[str, Any]]:
    """
    在配置中查找 Skill

    Returns:
        (category, skill_data) 或 None
    """
    skills = config.get("skills", {})
    for category, category_skills in skills.items():
        if skill_name in category_skills:
            return category, category_skills[skill_name]
    return None, None


def rename_skill_file(skills_dir: Path, skill_name: str, enable: bool = True) -> None:
    """
    重命名 Skill 文件

    Args:
        skills_dir: Skills 目录
        skill_name: Skill 名称
        enable: True=启用, False=禁用
    """
    skill_dir = skills_dir / skill_name

    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill 目录不存在: {skill_dir}")

    if enable:
        # 启用: (DISABLED)SKILL.md → SKILL.md
        source_file = skill_dir / "(DISABLED)SKILL.md"
        target_file = skill_dir / "SKILL.md"
    else:
        # 禁用: SKILL.md → (DISABLED)SKILL.md
        source_file = skill_dir / "SKILL.md"
        target_file = skill_dir / "(DISABLED)SKILL.md"

    if not source_file.exists():
        # 文件已经是目标状态,不需要重命名
        if target_file.exists():
            return  # 幂等性: 已经处于目标状态
        else:
            raise FileNotFoundError(
                f"源文件不存在: {source_file} (目标文件 {target_file} 也不存在)"
            )

    try:
        source_file.rename(target_file)
    except OSError as e:
        raise OSError(
            f"无法重命名文件 (文件被占用或权限不足): {source_file} → {target_file}\n错误: {str(e)}"
        )


def disable_skill(skill_name: str, config_path: str = None, skills_dir: str = None) -> int:
    """
    禁用 Skill

    Returns:
        退出码
    """
    try:
        # 加载配置
        config_file = find_config_file(config_path)
        config = load_config(config_file)

        # 查找 Skill
        category, skill_data = find_skill_in_config(config, skill_name)
        if category is None:
            print(f"错误: Skill '{skill_name}' 不存在于配置中", file=sys.stderr)
            return 1

        # 检查是否已禁用
        if not skill_data.get("enabled", False):
            print(f"Skill '{skill_name}' 已禁用 (幂等操作)")
            return 0

        # 更新配置 (保留 API 密钥)
        config["skills"][category][skill_name]["enabled"] = False
        save_config(config_file, config)

        # 重命名文件
        if skills_dir:
            skills_path = Path(skills_dir)
        else:
            skills_path = Path(".claude/skills")

        try:
            rename_skill_file(skills_path, skill_name, enable=False)
        except FileNotFoundError as e:
            print(f"警告: {str(e)}", file=sys.stderr)
            print(f"配置已更新,但文件重命名失败", file=sys.stderr)
        except OSError as e:
            print(f"错误: {str(e)}", file=sys.stderr)
            # 回滚配置
            config["skills"][category][skill_name]["enabled"] = True
            save_config(config_file, config)
            return 2

        print(f"❌ Skill '{skill_name}' 已禁用")
        if skill_data.get("requires_api", False) and skill_data.get("api_key"):
            print(f"   API 密钥已保留,下次启用时无需重新配置")
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


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="禁用指定的 ElecSpeckit Skill")
    parser.add_argument("skill_name", type=str, help="Skill 名称")
    parser.add_argument(
        "--config",
        type=str,
        help="skill_config.json 文件路径 (默认: .elecspecify/memory/skill_config.json)",
    )
    parser.add_argument(
        "--skills-dir", type=str, help="Skills 目录路径 (默认: .claude/skills/)"
    )

    args = parser.parse_args()

    return disable_skill(args.skill_name, args.config, args.skills_dir)


if __name__ == "__main__":
    sys.exit(main())
