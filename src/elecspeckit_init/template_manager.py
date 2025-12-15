"""
模板管理模块

负责复制和管理 ElecSpeckit 项目模板
"""

from pathlib import Path
from typing import List

from .fs_utils import (
    ChangeSummary,
    FileChange,
    copy_directory_tree,
    ensure_directory_exists,
    write_or_update_file,
)

# 模板目录位于包内
TEMPLATE_ROOT = Path(__file__).resolve().parent / "templates"


# Agent 平台配置
AGENT_CONFIG = {
    "claude": {"dir_name": ".claude", "commands_dir": "commands", "file_extension": ".md"},
    "qwen": {"dir_name": ".qwen", "commands_dir": "commands", "file_extension": ".toml"},
}


# 命令模板基础名称
COMMAND_BASENAMES = [
    "elecspeckit.constitution",
    "elecspeckit.specify",
    "elecspeckit.plan",
    "elecspeckit.tasks",
    "elecspeckit.docs",
    "elecspeckit.clarify",
    "elecspeckit.checklist",
    "elecspeckit.analyze",
]


def initialize_project_structure(
    base_dir: Path, platform: str, create_backup: bool = False
) -> ChangeSummary:
    """
    初始化完整的项目结构

    Args:
        base_dir: 项目根目录
        platform: Agent 平台 ("claude" 或 "qwen")
        create_backup: 是否创建备份

    Returns:
        ChangeSummary 包含所有文件变更记录
    """
    summary = ChangeSummary(changes=[])

    # 1. 创建 .elecspecify/ 基础结构
    elecspecify_changes = _create_elecspecify_structure(base_dir, create_backup)
    for change in elecspecify_changes:
        summary.add_change(change)

    # 2. 创建 Agent 平台目录和命令模板
    agent_changes = _create_agent_commands(base_dir, platform, create_backup)
    for change in agent_changes:
        summary.add_change(change)

    return summary


def _create_elecspecify_structure(base_dir: Path, create_backup: bool) -> List[FileChange]:
    """
    创建 .elecspecify/ 基础结构

    包括:
    - .elecspecify/memory/constitution.md
    - .elecspecify/scripts/powershell/
    - .elecspecify/templates/ (spec-template.md, plan-template.md, etc.)
    """
    changes: List[FileChange] = []

    elecspecify_dir = base_dir / ".elecspecify"
    memory_dir = elecspecify_dir / "memory"
    scripts_dir = elecspecify_dir / "scripts" / "powershell"
    templates_dir = elecspecify_dir / "templates"

    # 创建目录
    ensure_directory_exists(memory_dir)
    ensure_directory_exists(scripts_dir)
    ensure_directory_exists(templates_dir)

    # 复制 elecspecify 模板
    elecspecify_template_dir = TEMPLATE_ROOT / "elecspecify"

    if elecspecify_template_dir.exists():
        # 复制 constitution-template.md
        constitution_source = elecspecify_template_dir / "constitution-template.md"
        if constitution_source.exists():
            constitution_target = memory_dir / "constitution.md"
            content = constitution_source.read_text(encoding="utf-8")

            # 只在文件不存在或为空时创建
            if (
                not constitution_target.exists()
                or not constitution_target.read_text(encoding="utf-8").strip()
            ):
                change = write_or_update_file(
                    constitution_target, content, create_backup=False  # 首次创建不需要备份
                )
                changes.append(change)

        # 复制 skill_config_template.json (仅 Claude 平台)
        skill_config_source = elecspecify_template_dir / "skill_config_template.json"
        if skill_config_source.exists():
            skill_config_target = memory_dir / "skill_config.json"
            content = skill_config_source.read_text(encoding="utf-8")

            # 只在文件不存在或为空时创建
            if (
                not skill_config_target.exists()
                or not skill_config_target.read_text(encoding="utf-8").strip()
            ):
                change = write_or_update_file(
                    skill_config_target, content, create_backup=False
                )
                changes.append(change)

                # T058.1: 设置文件权限为 0600（仅文件所有者可读写）
                _set_skill_config_permissions(skill_config_target)

        # 复制模板文件到 templates/ 目录
        template_files = [
            "spec-template.md",
            "plan-template.md",
            "tasks-template.md",
            "checklist-template.md",
        ]

        for template_file in template_files:
            source = elecspecify_template_dir / template_file
            if source.exists():
                target = templates_dir / template_file
                content = source.read_text(encoding="utf-8")

                if not target.exists() or not target.read_text(encoding="utf-8").strip():
                    change = write_or_update_file(target, content, create_backup=False)
                    changes.append(change)

        # 复制 scripts 目录 (包含查询脚本)
        scripts_source_dir = elecspecify_template_dir / "scripts"
        if scripts_source_dir.exists():
            scripts_target_dir = elecspecify_dir / "scripts"
            # 使用 copy_directory_tree 复制整个 scripts 目录树
            script_changes = copy_directory_tree(
                scripts_source_dir, scripts_target_dir, create_backup=create_backup
            )
            for change in script_changes.changes:
                changes.append(change)

    return changes


def _create_agent_commands(base_dir: Path, platform: str, create_backup: bool) -> List[FileChange]:
    """
    创建 Agent 平台命令模板

    Args:
        base_dir: 项目根目录
        platform: Agent 平台
        create_backup: 是否创建备份

    Returns:
        文件变更列表
    """
    changes: List[FileChange] = []

    if platform not in AGENT_CONFIG:
        raise ValueError(f"不支持的平台: {platform}")

    config = AGENT_CONFIG[platform]
    platform_dir = base_dir / config["dir_name"]
    commands_dir = platform_dir / config["commands_dir"]

    # 创建目录
    ensure_directory_exists(commands_dir)

    # 部署 Skills (仅 Claude 平台)
    if platform == "claude":
        try:
            skills_summary = deploy_skills_to_claude(base_dir, create_backup)
            for change in skills_summary.changes:
                changes.append(change)
        except RuntimeError as e:
            # Skills 库不完整时记录警告但不中断初始化
            import sys
            print(f"警告: {e}", file=sys.stderr)

    # 复制命令模板
    template_dir = TEMPLATE_ROOT / platform

    if template_dir.exists():
        for command_name in COMMAND_BASENAMES:
            template_file = template_dir / f"{command_name}{config['file_extension']}"

            if template_file.exists():
                target_file = commands_dir / f"{command_name}{config['file_extension']}"
                content = template_file.read_text(encoding="utf-8")

                change = write_or_update_file(target_file, content, create_backup=create_backup)
                changes.append(change)
            else:
                # 如果模板不存在,创建占位符
                target_file = commands_dir / f"{command_name}{config['file_extension']}"
                content = _generate_placeholder_content(command_name, platform)

                change = write_or_update_file(target_file, content, create_backup=create_backup)
                changes.append(change)

    return changes


def _generate_placeholder_content(command_name: str, platform: str) -> str:
    """
    生成占位符内容

    当模板文件不存在时,生成占位符内容
    """
    if platform == "claude":
        return f"""# /{command_name}

本文件由 `elecspeckit --init` 自动生成,用于在当前项目中接入 ElecSpeckit 工作流。

此为占位符模板,待正式模板文件准备完成后将自动更新。

---

Generated by ElecSpeckit CLI
"""
    elif platform == "qwen":
        return f"""description = "ElecSpeckit command: {command_name}"

prompt = \"\"\"
/{command_name}

本文件由 `elecspeckit --init` 自动生成,用于在当前项目中接入 ElecSpeckit 工作流。

此为占位符模板,待正式模板文件准备完成后将自动更新。

Generated by ElecSpeckit CLI
\"\"\"
"""
    else:
        return f"# {command_name}\n\nPlaceholder content"


def detect_platform(base_dir: Path) -> str | None:
    """
    检测项目使用的 Agent 平台

    Args:
        base_dir: 项目根目录

    Returns:
        检测到的平台名称,如果未检测到则返回 None
    """
    for platform, config in AGENT_CONFIG.items():
        platform_dir = base_dir / config["dir_name"]
        if platform_dir.exists() and platform_dir.is_dir():
            return platform

    return None


def detect_all_platforms(base_dir: Path) -> list[str]:
    """
    检测项目中所有存在的 Agent 平台

    Args:
        base_dir: 项目根目录

    Returns:
        检测到的所有平台名称列表
    """
    detected_platforms = []

    for platform, config in AGENT_CONFIG.items():
        platform_dir = base_dir / config["dir_name"]
        if platform_dir.exists() and platform_dir.is_dir():
            detected_platforms.append(platform)

    return detected_platforms


def check_multi_platform_conflict(base_dir: Path) -> tuple[bool, list[str]]:
    """
    检查是否存在多平台配置冲突

    根据 spec.md 约束,v1.x 版本仅支持单平台架构
    如果同时检测到 .claude/ 和 .qwen/ 目录,则存在冲突

    Args:
        base_dir: 项目根目录

    Returns:
        (是否存在冲突, 检测到的平台列表) 元组
    """
    detected = detect_all_platforms(base_dir)

    if len(detected) > 1:
        return True, detected

    return False, detected


# FR-006 定义的 23 个 Skills 清单
REQUIRED_SKILLS = [
    # 信息检索 (5)
    "docs-seeker",
    "arxiv-search",
    "web-research",
    "perplexity-search",
    "openalex-database",
    # 文档生成 (7)
    "docx",
    "pdf",
    "xlsx",
    "pptx",
    "architecture-diagrams",
    "mermaid-tools",
    "docs-write",
    # 数据分析 (2)
    "hardware-data-analysis",
    "citation-management",
    # 嵌入式系统 (4)
    "embedded-systems",
    "hardware-protocols",
    "esp32-embedded-dev",
    "embedded-best-practices",
    # 元器件采购 (1)
    "mouser-component-search",
    # 领域分析 (3)
    "circuit-commutation-analysis",
    "thermal-simulation",
    "emc-analysis",
    # 元 Skill (1)
    "skill-creator",
]


def verify_skills_source_integrity() -> tuple[bool, list[str]]:
    """
    验证源 Skills 库完整性 (T057.1)

    检查模板目录是否包含 FR-006 定义的全部 23 个 Skills

    Returns:
        (是否完整, 缺失的 Skills 列表) 元组
    """
    skills_source_dir = TEMPLATE_ROOT / "elecspecify" / "skills"

    if not skills_source_dir.exists():
        return False, REQUIRED_SKILLS

    missing_skills = []
    for skill_name in REQUIRED_SKILLS:
        skill_md = skills_source_dir / skill_name / "SKILL.md"
        if not skill_md.exists():
            missing_skills.append(skill_name)

    return len(missing_skills) == 0, missing_skills


def deploy_skills_to_claude(
    base_dir: Path, create_backup: bool = False
) -> ChangeSummary:
    """
    部署 Skills 到 .claude/skills/ 目录 (T057, T060)

    Args:
        base_dir: 项目根目录
        create_backup: 是否创建备份（升级模式）

    Returns:
        ChangeSummary 包含所有文件变更记录

    Raises:
        RuntimeError: 源 Skills 库不完整时抛出异常
    """
    # T057.1: 验证源 Skills 库完整性
    is_complete, missing_skills = verify_skills_source_integrity()
    if not is_complete:
        raise RuntimeError(
            f"源 Skills 库不完整，缺失以下 Skills: {', '.join(missing_skills)}\n"
            f"请确保 templates/elecspecify/skills/ 目录包含全部 23 个 Skills"
        )

    summary = ChangeSummary(changes=[])

    skills_source_dir = TEMPLATE_ROOT / "elecspecify" / "skills"
    skills_target_dir = base_dir / ".claude" / "skills"

    # 确保目标目录存在
    ensure_directory_exists(skills_target_dir)

    # T062: 升级时创建备份
    if create_backup and skills_target_dir.exists():
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = base_dir / ".elecspecify" / "backup" / f"skills.bak.{timestamp}"
        ensure_directory_exists(backup_dir.parent)

        # 备份现有 Skills 目录
        if any(skills_target_dir.iterdir()):
            import shutil

            shutil.copytree(skills_target_dir, backup_dir, dirs_exist_ok=True)

            # 记录备份信息
            summary.add_change(
                FileChange(
                    path=backup_dir,
                    status="backed_up",
                    message=f"备份旧的 Skills 目录到 {backup_dir.relative_to(base_dir)}",
                )
            )

    # T060: 完整复制 Skills（包含子目录、Python 脚本、references/）
    skills_changes = copy_directory_tree(
        skills_source_dir, skills_target_dir, create_backup=False
    )

    for change in skills_changes.changes:
        summary.add_change(change)

    return summary


def _set_skill_config_permissions(skill_config_path: Path) -> None:
    """
    设置 skill_config.json 文件权限为 0600 (T058.1)

    仅文件所有者可读写，保护 API 密钥安全

    Args:
        skill_config_path: skill_config.json 文件路径
    """
    import os
    import sys

    try:
        if sys.platform == "win32":
            # Windows: 使用 icacls 设置权限
            import subprocess

            # 移除所有继承权限，只保留当前用户的完全控制权限
            subprocess.run(
                [
                    "icacls",
                    str(skill_config_path),
                    "/inheritance:r",
                    "/grant:r",
                    f"{os.environ.get('USERNAME', 'Administrator')}:F",
                ],
                check=False,
                capture_output=True,
            )
        else:
            # Unix-like: 使用 chmod 设置 0600 权限
            os.chmod(skill_config_path, 0o600)
    except Exception:
        # 权限设置失败不中断流程，只是失去安全保护
        pass
