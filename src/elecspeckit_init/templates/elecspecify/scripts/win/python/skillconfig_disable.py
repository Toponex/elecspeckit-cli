#!/usr/bin/env python3
"""
skillconfig_disable.py - 禁用 Skill

用法:
    python skillconfig_disable.py <skill_name>

功能:
    1. 更新 skill_config.json 中 enabled: false
    2. 重命名 SKILL.md → (DISABLED)SKILL.md
    3. 保留 API 密钥配置
    4. Claude Code 停止加载此 Skill

退出码:
    0: 成功（包括已禁用的幂等操作）
    1: Skill 不存在
    2: 文件重命名失败（权限问题或文件被占用）
"""

import json
import sys
from pathlib import Path


def find_project_root():
    """从当前目录向上查找项目根目录"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".elecspecify").exists():
            return current
        current = current.parent
    return None


def disable_skill(skill_name):
    """禁用 Skill"""
    project_root = find_project_root()
    if not project_root:
        print("错误: 未找到 ElecSpecKit 项目根目录", file=sys.stderr)
        print("提示: 请在项目目录中运行此命令", file=sys.stderr)
        sys.exit(1)

    config_file = project_root / ".elecspecify" / "memory" / "skill_config.json"
    skills_dir = project_root / ".claude" / "skills"

    if not config_file.exists():
        print(f"错误: 配置文件不存在: {config_file}", file=sys.stderr)
        sys.exit(1)

    # 读取配置
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件 JSON 格式错误: {e}", file=sys.stderr)
        sys.exit(4)

    # 查找 Skill
    found = False
    skill_category = None
    skill_config = None

    for category, skills in config.get("skills", {}).items():
        if skill_name in skills:
            found = True
            skill_category = category
            skill_config = skills[skill_name]
            break

    if not found:
        print(f"错误: Skill '{skill_name}' 不存在", file=sys.stderr)
        sys.exit(1)

    # 检查是否已禁用（幂等性）
    already_disabled = not skill_config.get("enabled", False)

    # 更新 enabled 状态（保留 API 密钥）
    skill_config["enabled"] = False

    # 写回配置文件
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        print(f"错误: 无法写入配置文件: {e}", file=sys.stderr)
        sys.exit(2)

    # 重命名 SKILL.md 文件
    skill_dir = skills_dir / skill_name
    skill_md = skill_dir / "SKILL.md"
    disabled_skill_md = skill_dir / "(DISABLED)SKILL.md"

    file_renamed = False

    if skill_md.exists():
        try:
            skill_md.rename(disabled_skill_md)
            file_renamed = True
        except Exception as e:
            print(f"错误: 无法重命名文件: {e}", file=sys.stderr)
            print(f"  {skill_md} → {disabled_skill_md}", file=sys.stderr)
            # 回滚配置更改
            skill_config["enabled"] = not already_disabled
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                f.write("\n")
            sys.exit(2)

    # 输出结果
    if already_disabled and not file_renamed:
        print(f"❌ Skill '{skill_name}' 已禁用（幂等操作）")
    else:
        print(f"❌ Skill '{skill_name}' 已禁用")
        if file_renamed:
            print(f"   文件已重命名: SKILL.md → (DISABLED)SKILL.md")
        print(f"   Claude Code 不再加载此 Skill")

        # 检查是否保留了 API 密钥
        if skill_config.get("requires_api", False) and skill_config.get("api_key", "").strip():
            print(f"   API 密钥已保留，重新启用时无需重新配置")

    sys.exit(0)


if __name__ == "__main__":
    # 设置 UTF-8 输出（Windows 兼容性）
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    import argparse

    parser = argparse.ArgumentParser(description="禁用 ElecSpecKit Skill")
    parser.add_argument("skill_name", help="Skill 名称（例如：perplexity-search）")

    args = parser.parse_args()

    disable_skill(args.skill_name)
