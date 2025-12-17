#!/usr/bin/env python3
"""
skillconfig_update.py - 安全更新 Skill 配置（主要是 API 密钥）

用法:
    python skillconfig_update.py <skill_name> --api-key <API_KEY>
    python skillconfig_update.py <skill_name> --api-key ""  # 清空 API 密钥

功能:
    1. 更新 skill_config.json 中的 api_key 字段
    2. 同步更新 .claude/skills/<skill>/SKILL.md 的 frontmatter（让 Claude 立即识别）
    3. 使用原子性更新机制（临时文件 → 验证 → 替换）
    4. 自动调用 skillconfig_validate.py 验证配置
    5. 验证失败时自动回滚

退出码:
    0: 成功
    1: Skill 不存在或不需要 API
    2: 权限问题
    3: 验证失败，已回滚
    4: JSON 格式错误
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def find_project_root():
    """从当前目录向上查找项目根目录"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".elecspecify").exists():
            return current
        current = current.parent
    return None


def update_skill_frontmatter(skill_path, api_key):
    """
    更新 SKILL.md 的 frontmatter 中的 api_key 字段

    Args:
        skill_path: SKILL.md 文件路径
        api_key: API 密钥值

    Returns:
        True if updated, False otherwise
    """
    if not skill_path.exists():
        return False

    try:
        content = skill_path.read_text(encoding="utf-8")

        # 匹配 frontmatter (YAML格式)
        frontmatter_pattern = r"^---\n(.*?)\n---"
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if not match:
            return False

        frontmatter = match.group(1)
        rest_content = content[match.end():]

        # 更新或添加 api_key 字段
        api_key_pattern = r"^api_key:.*$"

        if re.search(api_key_pattern, frontmatter, re.MULTILINE):
            # 已存在 api_key 字段，替换它
            new_frontmatter = re.sub(
                api_key_pattern,
                f'api_key: "{api_key}"',
                frontmatter,
                flags=re.MULTILINE
            )
        else:
            # 不存在 api_key 字段，在 requires_api 后添加
            requires_api_pattern = r"(^requires_api:.*$)"
            new_frontmatter = re.sub(
                requires_api_pattern,
                rf'\1\napi_key: "{api_key}"',
                frontmatter,
                flags=re.MULTILINE
            )

        # 重新组装文件内容
        new_content = f"---\n{new_frontmatter}\n---{rest_content}"

        # 写回文件
        skill_path.write_text(new_content, encoding="utf-8")
        return True

    except Exception as e:
        print(f"警告: 无法更新 SKILL.md frontmatter: {e}", file=sys.stderr)
        return False


def update_skill_config(skill_name, api_key):
    """更新 Skill 配置"""
    project_root = find_project_root()
    if not project_root:
        print("错误: 未找到 ElecSpecKit 项目根目录", file=sys.stderr)
        print("提示: 请在项目目录中运行此命令", file=sys.stderr)
        sys.exit(1)

    config_file = project_root / ".elecspecify" / "memory" / "skill_config.json"

    if not config_file.exists():
        print(f"错误: 配置文件不存在: {config_file}", file=sys.stderr)
        print("提示: 请运行 'elecspeckit init' 初始化项目", file=sys.stderr)
        sys.exit(1)

    # 读取现有配置
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
        print(f"提示: 运行 'python skillconfig_list.py' 查看所有可用 Skills", file=sys.stderr)
        sys.exit(1)

    if not skill_config.get("requires_api", False):
        print(f"错误: Skill '{skill_name}' 不需要 API 密钥", file=sys.stderr)
        sys.exit(1)

    # 更新 API 密钥
    old_api_key = skill_config.get("api_key", "")
    skill_config["api_key"] = api_key

    # 同步更新 SKILL.md frontmatter
    skills_dir = project_root / ".claude" / "skills"
    skill_md_path = skills_dir / skill_name / "SKILL.md"
    disabled_skill_md_path = skills_dir / skill_name / "(DISABLED)SKILL.md"

    frontmatter_updated = False
    if skill_md_path.exists():
        frontmatter_updated = update_skill_frontmatter(skill_md_path, api_key)
    elif disabled_skill_md_path.exists():
        frontmatter_updated = update_skill_frontmatter(disabled_skill_md_path, api_key)

    # 原子性更新：写入临时文件
    temp_file = config_file.with_suffix(".tmp.json")
    backup_file = None

    try:
        # 创建备份
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_file = config_file.with_suffix(f".json.bak.{timestamp}")
        shutil.copy2(config_file, backup_file)

        # 写入临时文件
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write("\n")  # 添加结尾换行

        # 验证临时文件
        validate_script = config_file.parent.parent.parent / "scripts" / "win" / "python" / "skillconfig_validate.py"

        if validate_script.exists():
            # 临时替换配置文件进行验证
            shutil.move(str(config_file), str(config_file.with_suffix(".json.old")))
            shutil.copy2(str(temp_file), str(config_file))

            result = subprocess.run(
                [sys.executable, str(validate_script)],
                capture_output=True,
                text=True,
                timeout=10
            )

            # 恢复原文件
            shutil.move(str(config_file.with_suffix(".json.old")), str(config_file))

            if result.returncode != 0:
                print(f"错误: 配置验证失败，已回滚到原配置", file=sys.stderr)
                print(f"验证输出: {result.stdout}", file=sys.stderr)
                if temp_file.exists():
                    temp_file.unlink()
                sys.exit(3)

        # 验证通过，替换原文件
        shutil.copy2(str(temp_file), str(config_file))

        # 清理临时文件
        if temp_file.exists():
            temp_file.unlink()

        # 设置文件权限（仅所有者可读写）
        try:
            if sys.platform != "win32":
                os.chmod(config_file, 0o600)
            else:
                # Windows: 使用 icacls 设置权限
                subprocess.run(
                    [
                        "icacls",
                        str(config_file),
                        "/inheritance:r",
                        "/grant:r",
                        f"{os.environ.get('USERNAME', 'Administrator')}:F",
                    ],
                    check=False,
                    capture_output=True,
                )
        except Exception:
            pass  # 权限设置失败不阻塞

        # 输出成功信息
        print(f"✅ Skill '{skill_name}' 配置已更新")

        if api_key:
            print(f"   API 密钥已设置 (长度: {len(api_key)} 字符)")
        else:
            print(f"   API 密钥已清空")

        print(f"   配置文件: {config_file}")
        print(f"   备份文件: {backup_file.name}")

        if frontmatter_updated:
            print(f"   ✓ SKILL.md frontmatter 已同步更新")
            print(f"   ✓ Claude Code 将立即识别新的 API 密钥（无需重启）")
        else:
            print(f"   ⚠ 警告: 无法更新 SKILL.md frontmatter")
            print(f"   提示: 可能需要重启 Claude Code 才能识别新的 API 密钥")

        return 0

    except PermissionError as e:
        print(f"错误: 权限不足，无法写入配置文件: {e}", file=sys.stderr)
        # 恢复备份
        if backup_file and backup_file.exists():
            shutil.copy2(backup_file, config_file)
        if temp_file.exists():
            temp_file.unlink()
        sys.exit(2)

    except Exception as e:
        print(f"错误: 更新配置失败: {e}", file=sys.stderr)
        # 恢复备份
        if backup_file and backup_file.exists():
            shutil.copy2(backup_file, config_file)
        if temp_file.exists():
            temp_file.unlink()
        sys.exit(5)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="更新 ElecSpecKit Skill 配置")
    parser.add_argument("skill_name", help="Skill 名称（例如：perplexity-search）")
    parser.add_argument(
        "--api-key",
        required=True,
        help="API 密钥（使用空字符串清空）"
    )

    args = parser.parse_args()

    update_skill_config(args.skill_name, args.api_key)


if __name__ == "__main__":
    # 设置 UTF-8 输出（Windows 兼容性）
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    main()
