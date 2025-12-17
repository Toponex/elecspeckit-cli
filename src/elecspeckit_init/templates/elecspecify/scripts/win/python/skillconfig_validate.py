#!/usr/bin/env python3
"""
skillconfig_validate.py - 验证 Skills 配置一致性

用法:
    python skillconfig_validate.py

验证内容:
    1. skill_config.json 文件格式正确
    2. 配置中的每个 Skill 目录存在
    3. enabled: true 的 Skill 有 SKILL.md 文件
    4. enabled: false 的 Skill 可以有 SKILL.md 或没有（灵活）
    5. Skills 目录中的 Skill 都在配置中（警告）

输出格式 (JSON):
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


def validate_skill_config():
    """验证 Skill 配置"""
    project_root = find_project_root()
    if not project_root:
        result = {
            "status": "invalid",
            "errors": [{"skill": "system", "error": "未找到 ElecSpecKit 项目根目录"}],
            "warnings": []
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    config_file = project_root / ".elecspecify" / "memory" / "skill_config.json"
    skills_dir = project_root / ".claude" / "skills"

    errors = []
    warnings = []

    # 检查配置文件存在
    if not config_file.exists():
        result = {
            "status": "invalid",
            "errors": [{"skill": "system", "error": f"配置文件不存在: {config_file}"}],
            "warnings": []
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    # 检查 JSON 格式
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        result = {
            "status": "invalid",
            "errors": [{"skill": "system", "error": f"JSON 格式错误: {e}"}],
            "warnings": []
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(4)

    # 检查 Skills 目录存在
    if not skills_dir.exists():
        warnings.append({
            "skill": "system",
            "warning": f"Skills 目录不存在: {skills_dir}（可能尚未部署 Skills）"
        })

    # 收集配置中的所有 Skills
    configured_skills = set()
    for category, skills in config.get("skills", {}).items():
        for skill_name, skill_config in skills.items():
            configured_skills.add(skill_name)

            if skills_dir.exists():
                skill_dir = skills_dir / skill_name

                # 检查 Skill 目录存在
                if not skill_dir.exists():
                    errors.append({
                        "skill": skill_name,
                        "error": f"Skill 目录不存在: {skill_dir}"
                    })
                    continue

                # 检查 SKILL.md 文件
                skill_md = skill_dir / "SKILL.md"
                disabled_skill_md = skill_dir / "(DISABLED)SKILL.md"
                enabled = skill_config.get("enabled", False)

                if enabled:
                    # 已启用的 Skill 应该有 SKILL.md
                    if not skill_md.exists():
                        if disabled_skill_md.exists():
                            errors.append({
                                "skill": skill_name,
                                "error": "enabled: true 但文件名为 (DISABLED)SKILL.md"
                            })
                        else:
                            errors.append({
                                "skill": skill_name,
                                "error": "enabled: true 但 SKILL.md 不存在"
                            })
                else:
                    # 已禁用的 Skill 应该有 (DISABLED)SKILL.md
                    if skill_md.exists():
                        warnings.append({
                            "skill": skill_name,
                            "warning": "enabled: false 但文件名为 SKILL.md（应为 (DISABLED)SKILL.md）"
                        })

                # 检查 API 密钥
                requires_api = skill_config.get("requires_api", False)
                has_api_key = bool(skill_config.get("api_key", "").strip())

                if enabled and requires_api and not has_api_key:
                    warnings.append({
                        "skill": skill_name,
                        "warning": "Skill 已启用且需要 API 密钥，但未配置 API 密钥"
                    })

    # 检查 Skills 目录中未在配置的 Skills
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and skill_dir.name not in configured_skills:
                if skill_dir.name != "README.md":  # 忽略 README
                    warnings.append({
                        "skill": skill_dir.name,
                        "warning": "Skills 目录中存在但未在配置中"
                    })

    # 构造结果
    result = {
        "status": "valid" if len(errors) == 0 else "invalid",
        "errors": errors,
        "warnings": warnings
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if len(errors) > 0:
        sys.exit(3)
    else:
        sys.exit(0)


if __name__ == "__main__":
    # 设置 UTF-8 输出（Windows 兼容性）
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    validate_skill_config()
