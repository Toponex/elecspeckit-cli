#!/usr/bin/env python3
"""
skillconfig_update.py - 更新 Skill 配置 (如 API 密钥)

功能:
- 更新 skill_config.json 中的配置字段 (如 api_key)
- 使用临时文件进行原子性更新
- 验证通过后才替换原文件
- 验证失败时删除临时文件并回滚
- 完成后自动调用 skillconfig_validate.py 验证

用法:
    python skillconfig_update.py <skill_name> --api-key <API_KEY> [--config CONFIG_FILE]

参数:
    skill_name: Skill 名称 (必需)
    --api-key: API 密钥 (必需)
    --config: skill_config.json 文件路径 (可选,默认 .elecspecify/memory/skill_config.json)

退出码:
    0: 成功
    1: 配置文件不存在或 Skill 不存在
    2: 文件权限问题
    3: 验证失败,已回滚
    4: JSON 格式错误
    5: 其他错误
"""

import json
import sys
import os
import subprocess
import tempfile
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


def validate_config_with_script(config_file: Path) -> bool:
    """
    调用 skillconfig_validate.py 验证配置

    Returns:
        True: 验证通过, False: 验证失败
    """
    validate_script = config_file.parent.parent.parent / "claude" / "scripts" / "win" / "python" / "skillconfig_validate.py"

    # 如果验证脚本不存在,尝试当前目录
    if not validate_script.exists():
        validate_script = Path(__file__).parent / "skillconfig_validate.py"

    if not validate_script.exists():
        print(f"警告: 找不到 skillconfig_validate.py,跳过验证", file=sys.stderr)
        return True  # 找不到验证脚本,假设验证通过

    try:
        # 调用验证脚本
        result = subprocess.run(
            [sys.executable, str(validate_script), "--config", str(config_file)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            return True
        else:
            print(f"验证失败:\n{result.stdout}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"警告: 验证超时,跳过验证", file=sys.stderr)
        return True
    except Exception as e:
        print(f"警告: 验证脚本执行失败: {str(e)}", file=sys.stderr)
        return True


def atomic_update_config(
    config_file: Path, config: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    原子性更新配置文件

    使用临时文件进行更新,验证通过后才替换原文件

    Returns:
        (success, message)
    """
    temp_file = None
    try:
        # 1. 创建临时文件
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".json", prefix="skill_config_", dir=config_file.parent
        )
        temp_file = Path(temp_path)

        # 2. 写入临时文件
        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # 3. 验证临时文件
        if not validate_config_with_script(temp_file):
            # 验证失败,删除临时文件
            temp_file.unlink()
            return False, "验证失败,配置未更新"

        # 4. 替换原文件
        try:
            # 保留原文件权限
            original_stat = config_file.stat()
            temp_file.replace(config_file)

            # 恢复权限
            os.chmod(config_file, original_stat.st_mode)

            return True, "配置已更新"

        except OSError as e:
            # 替换失败,清理临时文件
            if temp_file.exists():
                temp_file.unlink()
            return False, f"无法替换配置文件 (权限问题): {str(e)}"

    except Exception as e:
        # 任何错误都清理临时文件
        if temp_file and temp_file.exists():
            temp_file.unlink()
        return False, f"更新失败: {str(e)}"


def update_skill_config(
    skill_name: str, api_key: str, config_path: str = None
) -> int:
    """
    更新 Skill 配置

    Returns:
        退出码
    """
    try:
        # 加载配置
        config_file = find_config_file(config_path)
        original_config = load_config(config_file)

        # 查找 Skill
        category, skill_data = find_skill_in_config(original_config, skill_name)
        if category is None:
            print(f"错误: Skill '{skill_name}' 不存在于配置中", file=sys.stderr)
            return 1

        # 检查是否需要 API
        if not skill_data.get("requires_api", False):
            print(
                f"错误: Skill '{skill_name}' 不需要 API 密钥 (requires_api: false)",
                file=sys.stderr,
            )
            return 1

        # 更新配置
        updated_config = original_config.copy()
        updated_config["skills"][category][skill_name]["api_key"] = api_key

        # 原子性更新
        success, message = atomic_update_config(config_file, updated_config)

        if success:
            print(f"✅ Skill '{skill_name}' 配置已更新")
            if api_key:
                print(f"   API 密钥已设置")
            else:
                print(f"   API 密钥已清空")
            return 0
        else:
            print(f"错误: {message}", file=sys.stderr)
            print(f"配置已回滚到原状态", file=sys.stderr)
            return 3  # 验证失败

    except FileNotFoundError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件 JSON 格式错误\n{str(e)}", file=sys.stderr)
        return 4
    except PermissionError as e:
        print(f"错误: 权限不足\n{str(e)}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 5


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="更新 ElecSpeckit Skill 配置 (API 密钥等)")
    parser.add_argument("skill_name", type=str, help="Skill 名称")
    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="API 密钥 (设置为空字符串则清空密钥)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="skill_config.json 文件路径 (默认: .elecspecify/memory/skill_config.json)",
    )

    args = parser.parse_args()

    return update_skill_config(args.skill_name, args.api_key, args.config)


if __name__ == "__main__":
    sys.exit(main())
