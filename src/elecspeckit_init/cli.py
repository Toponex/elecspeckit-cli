"""
ElecSpeckit CLI 入口点

提供 elecspeckit 命令,支持以下子命令:
- init: 初始化 ElecSpeckit 项目结构
- check: 检查工具可用性
"""

import json as json_module
import sys
from pathlib import Path

import typer

# 修复Windows GBK编码问题: 强制UTF-8输出 (per T081 bug fix)
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        # 如果无法reconfigure，至少设置环境变量供子进程使用
        import os

        os.environ["PYTHONIOENCODING"] = "utf-8"
from rich import box
from rich.console import Console
from rich.panel import Panel

from .fs_utils import is_elecspeckit_project, is_empty_directory
from .git_utils import initialize_git_repo, is_git_available, is_git_repo
from .platform_utils import check_disk_space, setup_utf8_output
from .template_manager import (
    check_multi_platform_conflict,
    detect_platform,
    initialize_project_structure,
)
from .ui import InteractiveSelector

app = typer.Typer(
    name="elecspeckit",
    help="ElecSpeckit CLI - 硬件/电子项目规范驱动工作流工具",
    add_completion=False,
)
console = Console()


@app.command(name="init")
def init_command(
    platform: str = typer.Option(
        None, "--platform", "-p", help="指定 AI 平台 (claude/qwen), 跳过交互式选择"
    ),
    no_git: bool = typer.Option(False, "--no-git", help="跳过 git 仓库初始化"),
    reset: bool = typer.Option(False, "--reset", help="重置 constitution.md 到官方模板初始状态"),
    json_output: bool = typer.Option(False, "--json", help="以 JSON 格式输出结果"),
) -> None:
    """
    初始化 ElecSpeckit 项目结构

    在空目录中首次执行时,会显示交互式平台选择界面;
    在已有 ElecSpeckit 项目中执行时,会自动检测平台并更新模板。
    使用 --platform 参数可跳过交互式选择 (用于自动化/测试场景)。
    """
    try:
        result = _init_project(
            base_dir=Path.cwd(),
            platform=platform,
            no_git=no_git,
            reset=reset,
            json_output=json_output,
        )

        if json_output:
            # JSON 输出模式
            console.print(json_module.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 人类可读输出模式
            _print_init_result(result)

        # 根据结果设置退出码
        if result.get("status") == "error":
            raise typer.Exit(code=1)

    except KeyboardInterrupt:
        console.print("\n[yellow]操作已取消[/yellow]")
        raise typer.Exit(code=130)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(code=1)


def _init_project(
    base_dir: Path, platform: str, no_git: bool, reset: bool, json_output: bool
) -> dict:
    """
    初始化项目的核心逻辑

    Args:
        base_dir: 项目根目录
        platform: 指定的 AI 平台 (claude/qwen), None 表示交互式选择
        no_git: 是否跳过 git 初始化
        reset: 是否重置 constitution.md
        json_output: 是否输出 JSON 格式

    Returns:
        包含初始化结果的字典
    """
    # 检查目录状态
    is_empty = False
    is_existing_project = False

    try:
        is_empty = is_empty_directory(base_dir)
    except (FileNotFoundError, ValueError):
        pass

    try:
        is_existing_project = is_elecspeckit_project(base_dir)
    except FileNotFoundError:
        pass

    # 场景 1: 空目录 - 首次初始化
    if is_empty or (not is_existing_project):
        # 首次初始化时，静默忽略 --reset 标志 (per spec.md US2 AC5)
        return _init_new_project(base_dir, platform, no_git, reset, json_output)

    # 场景 2: 已有项目 - 升级模式
    return _upgrade_existing_project(base_dir, platform, no_git, reset, json_output)


def _init_new_project(
    base_dir: Path, platform: str, no_git: bool, reset: bool, json_output: bool
) -> dict:
    """
    在空目录中初始化新项目

    Args:
        base_dir: 项目根目录
        platform: 指定的 AI 平台 (claude/qwen), None 表示交互式选择
        no_git: 是否跳过 git 初始化
        reset: 是否重置 constitution.md (首次初始化时静默忽略)
        json_output: 是否输出 JSON 格式

    Returns:
        初始化结果字典
    """
    # 显示欢迎信息
    if not json_output:
        _print_welcome_banner(base_dir)

    # 平台选择: 优先使用 --platform 参数, 否则交互式选择
    if platform is None:
        # 交互式平台选择
        selector = InteractiveSelector(console)
        platform = selector.select_platform()

        if platform is None:
            return {"status": "cancelled", "message": "用户取消了初始化操作"}
    else:
        # 验证指定的平台参数
        if platform not in ["claude", "qwen"]:
            return {
                "status": "error",
                "message": f"无效的平台参数: {platform}, 仅支持 'claude' 或 'qwen'",
            }

    # 显示 Qwen 平台警告信息 (T022, 符合 SC-008.2 双语格式)
    if platform == "qwen" and not json_output:
        console.print(
            "[yellow]注意:[/yellow] Qwen 平台不支持 Claude Skills 功能，"
            "部分高级特性（如知识库自动查询、文档发现）将不可用\n"
        )

    # FR-047: 检查磁盘空间（部署前需 ≥ 100MB）
    enough, free_mb = check_disk_space(base_dir, required_mb=100)
    if not enough:
        error_msg = f"磁盘空间不足（剩余 {free_mb}MB），需要至少 100MB"
        if json_output:
            return {"status": "error", "message": error_msg, "disk_free_mb": free_mb, "disk_required_mb": 100}
        else:
            console.print(f"[red]错误:[/red] {error_msg}")
            return {"status": "error", "message": error_msg}

    # 初始化项目结构
    try:
        summary = initialize_project_structure(base_dir, platform, create_backup=False)

        # 提取文件列表
        files = [str(change.path.relative_to(base_dir)) for change in summary.changes]

        # Git 初始化 (处理所有场景)
        git_result = _handle_git_initialization(base_dir, platform, no_git, json_output)

        result = {
            "status": "success",
            "platform": platform,
            "mode": "new",
            "files": files,
            "files_created": summary.total_created,
            **git_result,  # 合并 git 相关结果
            "message": f"成功初始化 ElecSpeckit 项目 (平台: {platform})",
        }

        # 如果 --reset 标志被使用，记录它被静默忽略 (per spec.md US2 AC5)
        if reset:
            result["reset_constitution"] = False
            result["reset_ignored"] = True
            result["reset_ignore_reason"] = "首次初始化，--reset 标志被静默忽略"

        return result
    except Exception as e:
        return {"status": "error", "message": f"初始化失败: {e}"}


def detect_version_upgrade(base_dir: Path) -> dict:
    """
    检测项目是否需要版本升级 (T010)

    检测 v0.1.0 项目通过以下特征文件（按优先级顺序, per A8澄清）：
    1. .claude/commands/elecspeckit.kbconfig.md
    2. .qwen/commands/elecspeckit.kbconfig.toml
    3. .elecspecify/memory/knowledge-sources.json

    Args:
        base_dir: 项目根目录

    Returns:
        dict: {
            "is_upgrade": bool,          # 是否为升级路径
            "from_version": str | None,  # 源版本（如 "v0.1.0"）
            "trigger_file": str | None,  # 触发升级的特征文件（相对路径）
        }

    Examples:
        >>> result = detect_version_upgrade(Path.cwd())
        >>> if result["is_upgrade"]:
        ...     print(f"检测到从 {result['from_version']} 升级")
    """
    # 检测 v0.1.0 特征文件（按优先级顺序）
    v010_features = [
        base_dir / ".claude" / "commands" / "elecspeckit.kbconfig.md",
        base_dir / ".qwen" / "commands" / "elecspeckit.kbconfig.toml",
        base_dir / ".elecspecify" / "memory" / "knowledge-sources.json",
    ]

    for feature_file in v010_features:
        if feature_file.exists():
            return {
                "is_upgrade": True,
                "from_version": "v0.1.0",
                "trigger_file": str(feature_file.relative_to(base_dir)),
            }

    # 未检测到任何升级特征
    return {
        "is_upgrade": False,
        "from_version": None,
        "trigger_file": None,
    }


def _upgrade_existing_project(
    base_dir: Path, platform: str, no_git: bool, reset: bool, json_output: bool
) -> dict:
    """
    升级已有项目

    Args:
        base_dir: 项目根目录
        no_git: 是否跳过 git 初始化
        reset: 是否重置 constitution.md
        json_output: 是否输出 JSON 格式

    Returns:
        升级结果字典
    """
    # T025: 强制单平台约束检查
    has_conflict, detected_platforms = check_multi_platform_conflict(base_dir)

    if has_conflict:
        platforms_str = " 和 ".join([f".{p}/" for p in detected_platforms])
        error_message = (
            f"检测到多个 AI 平台配置({platforms_str} 同时存在)，" "请手工删除其中一个后重试"
        )

        if json_output:
            return {
                "status": "error",
                "error_type": "multi_platform_conflict",
                "detected_platforms": detected_platforms,
                "message": error_message,
            }
        else:
            console.print(f"\n[red]错误: {error_message}[/red]\n")
            console.print("[yellow]说明:[/yellow]")
            console.print("  ElecSpeckit v1.x 版本仅支持单平台架构")
            console.print(f"  当前检测到: {', '.join(detected_platforms)}")
            console.print("\n[cyan]解决方案:[/cyan]")
            console.print("  1. 确定要使用的平台 (claude 或 qwen)")
            console.print("  2. 删除另一个平台的目录")
            console.print("  3. 重新运行 elecspeckit init")

            return {
                "status": "error",
                "error_type": "multi_platform_conflict",
                "detected_platforms": detected_platforms,
                "message": error_message,
            }

    # 检测现有平台
    platform = detect_platform(base_dir)

    if platform is None:
        return {
            "status": "error",
            "message": "无法检测到现有 Agent 平台 (.claude/ 或 .qwen/ 目录不存在)",
        }

    if not json_output:
        console.print(f"\n[cyan]检测到现有 ElecSpeckit 项目 (平台: {platform})[/cyan]\n")

    # 处理 constitution.md 重置 (T062: --reset 标志功能)
    reset_result = None
    if reset:
        import shutil
        from datetime import datetime

        from .template_manager import TEMPLATE_ROOT

        constitution_file = base_dir / ".elecspecify" / "memory" / "constitution.md"

        if constitution_file.exists():
            try:
                # 显示警告提示
                if not json_output:
                    console.print("\n[yellow]⚠ 检测到 --reset 标志[/yellow]")
                    console.print("[dim]将重置 constitution.md 为官方模板初始状态[/dim]\n")

                # 读取模板内容
                template_file = TEMPLATE_ROOT / "elecspecify" / "constitution-template.md"
                if not template_file.exists():
                    error_msg = f"错误: 模板文件不存在: {template_file}"
                    if json_output:
                        reset_result = {"success": False, "error": error_msg}
                    else:
                        console.print(f"[red]{error_msg}[/red]")
                else:
                    template_content = template_file.read_text(encoding="utf-8")

                    # 创建带时间戳的备份 (格式: YYYYMMDD-HHMMSS, per spec.md FR-021)
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    backup_path = constitution_file.parent / f"constitution.md.bak.{timestamp}"

                    # 处理备份文件名冲突 (如果同名备份已存在，追加序号)
                    if backup_path.exists():
                        sequence = 1
                        while backup_path.exists():
                            backup_path = (
                                constitution_file.parent
                                / f"constitution.md.bak.{timestamp}.{sequence}"
                            )
                            sequence += 1

                    # 备份旧文件
                    try:
                        shutil.copy2(constitution_file, backup_path)
                    except (PermissionError, OSError) as e:
                        error_msg = f"无法创建备份: {e}"
                        if json_output:
                            reset_result = {"success": False, "error": error_msg}
                        else:
                            console.print(f"[red]错误: {error_msg}[/red]")
                        raise

                    # 写入新内容
                    try:
                        constitution_file.write_text(template_content, encoding="utf-8")
                        reset_result = {
                            "success": True,
                            "backup_file": backup_path.name,
                            "message": "constitution.md 已重置为官方模板",
                        }

                        if not json_output:
                            console.print("[green]✓[/green] constitution.md 已重置")
                            console.print(
                                f"[dim]  备份: .elecspecify/memory/{backup_path.name}[/dim]\n"
                            )

                    except (PermissionError, OSError) as e:
                        # 如果写入失败，尝试恢复备份
                        if backup_path.exists():
                            try:
                                shutil.copy2(backup_path, constitution_file)
                            except Exception:
                                pass
                        error_msg = f"无法写入 constitution.md: {e} (权限错误或文件只读)"
                        if json_output:
                            reset_result = {"success": False, "error": error_msg}
                        else:
                            console.print(f"[red]错误: {error_msg}[/red]")
                        raise

            except Exception as e:
                # 如果 reset 失败，记录错误但不中断升级流程
                if reset_result is None:
                    reset_result = {"success": False, "error": str(e)}
                if not json_output:
                    console.print(f"[yellow]警告: constitution.md 重置失败: {e}[/yellow]\n")
        else:
            # constitution.md 不存在时的处理
            if not json_output:
                console.print("[dim]constitution.md 不存在，跳过重置[/dim]\n")
            reset_result = {"success": False, "skipped": True, "reason": "constitution.md 不存在"}

    # FR-047: 检查磁盘空间（升级前需 ≥ 100MB）
    enough, free_mb = check_disk_space(base_dir, required_mb=100)
    if not enough:
        error_msg = f"磁盘空间不足（剩余 {free_mb}MB），需要至少 100MB"
        if json_output:
            return {"status": "error", "message": error_msg, "disk_free_mb": free_mb, "disk_required_mb": 100}
        else:
            console.print(f"[red]错误:[/red] {error_msg}")
            return {"status": "error", "message": error_msg}

    try:
        # 升级项目结构 (使用 create_backup=True 保护用户内容)
        summary = initialize_project_structure(base_dir, platform, create_backup=True)

        # 提取文件列表
        files = [str(change.path.relative_to(base_dir)) for change in summary.changes]

        # Git 初始化 (处理所有场景)
        git_result = _handle_git_initialization(base_dir, platform, no_git, json_output)

        result = {
            "status": "success",
            "platform": platform,
            "mode": "upgrade",
            "files": files,
            "files_updated": summary.total_updated,
            "files_backed_up": summary.total_backed_up,
            "files_skipped": summary.total_skipped,
            "reset_constitution": reset,
            **git_result,  # 合并 git 相关结果
            "message": f"成功升级 ElecSpeckit 项目 (平台: {platform})",
        }

        # 添加 reset 结果信息 (如果执行了 reset)
        if reset_result is not None:
            result["reset_result"] = reset_result

        return result

    except Exception as e:
        return {"status": "error", "message": f"升级失败: {e}"}


def _handle_git_initialization(
    base_dir: Path, platform: str, no_git: bool, json_output: bool
) -> dict:
    """
    处理 git 仓库初始化的所有场景

    Args:
        base_dir: 项目根目录
        platform: 平台名称 (claude/qwen)
        no_git: 是否跳过 git 初始化
        json_output: 是否 JSON 输出模式

    Returns:
        包含 git 初始化结果的字典
    """
    # 场景 1: 用户使用 --no-git 标志
    if no_git:
        if not json_output:
            console.print("[dim]Git 初始化已跳过 (--no-git 标志)[/dim]")

        return {
            "git_initialized": False,
            "git_message": "已跳过 (--no-git 标志)",
            "git_skipped": True,
            "git_skip_reason": "user_flag",
        }

    # 场景 2: git 不可用
    if not is_git_available():
        if not json_output:
            console.print(
                "[yellow]Git 未找到，已跳过仓库初始化。[/yellow]\n"
                "[dim]你可以稍后手动执行 `git init` 创建仓库。[/dim]"
            )

        return {
            "git_initialized": False,
            "git_message": "git 命令不可用,跳过 git 初始化",
            "git_skipped": True,
            "git_skip_reason": "git_not_available",
        }

    # 场景 3: 已有 git 仓库
    if is_git_repo(base_dir):
        if not json_output:
            console.print("[dim]检测到现有 git 仓库，已跳过 git 初始化[/dim]")

        return {
            "git_initialized": False,
            "git_message": "目录已经是 git 仓库,跳过 git 初始化",
            "git_skipped": True,
            "git_skip_reason": "existing_repo",
        }

    # 场景 4: 执行 git 初始化
    try:
        success, message = initialize_git_repo(
            base_dir, initial_commit_message=f"Initial ElecSpeckit project setup ({platform})"
        )

        if success:
            if not json_output:
                console.print("[green]✓[/green] Git 仓库已初始化并创建初始提交")

            return {"git_initialized": True, "git_message": message, "git_skipped": False}
        else:
            # git 初始化失败 (非阻塞)
            if not json_output:
                console.print(
                    f"[yellow]警告: git 初始化失败 - {message}[/yellow]\n"
                    "[dim]模板已成功生成，你可以稍后手动初始化 git 仓库。[/dim]"
                )

            return {
                "git_initialized": False,
                "git_message": message,
                "git_skipped": True,
                "git_skip_reason": "initialization_failed",
            }

    except Exception as e:
        # git 初始化异常 (非阻塞)
        error_message = f"git 初始化失败: {e}"

        if not json_output:
            console.print(
                f"[yellow]警告: {error_message}[/yellow]\n"
                "[dim]模板已成功生成，你可以稍后手动初始化 git 仓库。[/dim]"
            )

        return {
            "git_initialized": False,
            "git_message": error_message,
            "git_skipped": True,
            "git_skip_reason": "initialization_error",
        }


def _print_welcome_banner(base_dir: Path) -> None:
    """打印欢迎横幅"""
    banner = Panel(
        f"[bold cyan]ElecSpeckit CLI[/bold cyan]\n\n"
        f"硬件/电子项目规范驱动工作流工具\n\n"
        f"[dim]项目目录: {base_dir}[/dim]",
        title="欢迎使用",
        border_style="cyan",
        box=box.DOUBLE,
    )
    console.print(banner)
    console.print()


def _print_init_result(result: dict) -> None:
    """打印初始化结果"""
    status = result.get("status", "unknown")

    if status == "success":
        mode = result.get("mode", "unknown")

        console.print(f"[green]✓[/green] {result.get('message', '操作成功')}")

        # 显示详细信息
        if "platform" in result:
            console.print(f"  平台: [cyan]{result['platform']}[/cyan]")

        # 根据模式显示不同的文件统计
        if mode == "new":
            if "files_created" in result:
                console.print(f"  创建文件: {result['files_created']} 个")
        elif mode == "upgrade":
            if "files_updated" in result:
                console.print(f"  更新文件: {result['files_updated']} 个")
            if "files_backed_up" in result:
                console.print(f"  备份文件: {result['files_backed_up']} 个")
            if "files_skipped" in result:
                console.print(f"  跳过文件: {result['files_skipped']} 个")

        if "git_message" in result and result["git_message"]:
            git_status_color = "green" if result.get("git_initialized") else "yellow"
            console.print(
                f"  Git: [{git_status_color}]{result['git_message']}[/{git_status_color}]"
            )

        # T061: 显示 API 密钥提示 (仅 Claude 平台)
        if result.get("platform") == "claude":
            from pathlib import Path

            from .template_manager import get_api_required_skills

            try:
                api_skills = get_api_required_skills(Path.cwd())
                if api_skills:
                    console.print()
                    console.print("[yellow]⚠ API 密钥配置提示:[/yellow]")
                    console.print(
                        f"  检测到 {len(api_skills)} 个 Skills 需要 API 密钥才能使用：\n"
                    )
                    for skill in api_skills[:3]:  # 最多显示 3 个
                        console.print(f"  • [cyan]{skill['name']}[/cyan] - {skill['description']}")
                    if len(api_skills) > 3:
                        console.print(f"  [dim]  ...还有 {len(api_skills) - 3} 个 Skills[/dim]")

                    console.print(
                        "\n  [dim]配置方法: 编辑 [cyan].elecspecify/memory/skill_config.json[/cyan]，"
                        "在对应 Skill 的 [cyan]api_key[/cyan] 字段填写密钥[/dim]"
                    )
            except Exception:
                # 获取 API Skills 失败不影响主流程
                pass

        # 显示使用说明
        if mode == "new":
            usage_text = (
                "[dim]在 AI 助手 (Claude Code/Qwen Code) 中按以下顺序执行命令:[/dim]\n"
                "1. [cyan]/elecspeckit.kbconfig[/cyan] 验证当前配置\n"
                "   [dim]→ 配置外部知识源 (标准、参考设计、web API)[/dim]\n"
                "2. [cyan]/elecspeckit.constitution[/cyan] 补充项目约束\n"
                "   [dim]→ 定义设计原则、架构约束、质量标准[/dim]\n"
                "3. [cyan]/elecspeckit.specify[/cyan] <功能描述>\n"
                "   [dim]→ 生成特性规格 (spec.md)[/dim]\n"
                "4. [cyan]/elecspeckit.plan[/cyan]\n"
                "   [dim]→ 生成架构设计 (plan.md, research.md, data-model.md)[/dim]\n"
                "5. [cyan]/elecspeckit.tasks[/cyan]\n"
                "   [dim]→ 生成任务拆分 (tasks.md)[/dim]\n"
                "6. [cyan]/elecspeckit.docs[/cyan]\n"
                "   [dim]→ 生成多角色文档视图 (HW/BOM/Test/FA/PM/Datasheet/KB)[/dim]\n"
                "[yellow]提示:[/yellow] 可在各阶段使用 [cyan]/elecspeckit.clarify[/cyan] / "
                "[cyan]/elecspeckit.checklist[/cyan] / [cyan]/elecspeckit.analyze[/cyan] 提升质量\n"
                "[dim]详细文档: specs/001-elecspeckit-cli/quickstart.md[/dim]"
            )
            usage_panel = Panel(
                usage_text,
                title="[bold cyan]使用说明[/bold cyan]",
                border_style="cyan",
                padding=(0, 1),
            )
            console.print()
            console.print(usage_panel)
        elif mode == "upgrade":
            console.print("\n[bold]使用说明:[/bold]")
            console.print("  1. 检查更新后的模板文件")
            console.print("  2. 如有备份,对比差异: [cyan].elecspecify/**/*.bak.*[/cyan]")
            console.print("  3. 继续使用 ElecSpeckit 工作流")

    elif status == "cancelled":
        console.print("[yellow]操作已取消[/yellow]")

    elif status == "error":
        console.print(f"[red]错误: {result.get('message', '未知错误')}[/red]")


@app.command(name="check")
def check_command(
    json_output: bool = typer.Option(False, "--json", help="以 JSON 格式输出结果")
) -> None:
    """
    检查系统环境中所需工具的可用性

    检查项包括:
    - 必需工具: uv (包管理器)
    - 可选工具: git、claude、qwen
    - 脚本环境: PowerShell (Windows) 或 bash (Unix-like)
    """

    from .tool_checker import check_all_tools

    # 检测所有工具
    result = check_all_tools()

    if json_output:
        # JSON 输出模式
        _print_check_json(result)
    else:
        # 人类可读输出模式
        _print_check_tree(result)


def _print_check_tree(result: dict) -> None:
    """
    以树形结构输出工具检测结果

    Args:
        result: check_all_tools() 返回的结果
    """
    from rich.tree import Tree

    # 创建根节点
    tree = Tree("[bold cyan]ElecSpeckit CLI 工具检查[/bold cyan]")

    # 必需工具
    required_branch = tree.add("[bold]必需工具 (Required Tools)[/bold]")
    for tool in result["required_tools"]:
        _add_tool_to_tree(required_branch, tool)

    # 可选工具
    optional_branch = tree.add("[bold]可选工具 (Optional Tools)[/bold]")
    for tool in result["optional_tools"]:
        _add_tool_to_tree(optional_branch, tool)

    # Shell
    shell_branch = tree.add("[bold]脚本环境 (Shell)[/bold]")
    _add_tool_to_tree(shell_branch, result["shell"])

    # 输出树形结构
    console.print()
    console.print(tree)
    console.print()

    # 输出建议
    _print_check_suggestions(result)


def _add_tool_to_tree(branch, tool: dict) -> None:
    """
    将工具信息添加到树形分支

    Args:
        branch: 树形分支节点
        tool: 工具信息字典
    """
    if tool["available"]:
        # 可用工具 - 绿色 ●
        symbol = "[green]●[/green]"
        tool_text = f"{symbol} {tool['tool']}"

        if tool["version"]:
            tool_text += f" [dim](v{tool['version']})[/dim]"

        node = branch.add(tool_text)

        if tool["path"]:
            node.add(f"[dim]路径: {tool['path']}[/dim]")
    else:
        # 不可用工具 - 红色 ●
        symbol = "[red]●[/red]"
        tool_text = f"{symbol} {tool['tool']} [dim](未找到)[/dim]"
        branch.add(tool_text)


def _print_check_suggestions(result: dict) -> None:
    """
    输出工具安装建议

    Args:
        result: check_all_tools() 返回的结果
    """
    missing_tools = []

    # 检查必需工具
    for tool in result["required_tools"]:
        if not tool["available"]:
            missing_tools.append(("required", tool["tool"]))

    # 检查可选工具
    for tool in result["optional_tools"]:
        if not tool["available"]:
            missing_tools.append(("optional", tool["tool"]))

    # 检查 Shell
    if not result["shell"]["available"]:
        missing_tools.append(("shell", result["shell"]["tool"]))

    if missing_tools:
        console.print("[yellow]提示:[/yellow]")
        console.print()

        for category, tool_name in missing_tools:
            if category == "required":
                console.print(f"  [red]X[/red] {tool_name} [red](必需)[/red]")
                if tool_name == "uv":
                    console.print(
                        "    安装: https://docs.astral.sh/uv/getting-started/installation/"
                    )
            elif category == "optional":
                console.print(f"  [yellow]![/yellow] {tool_name} [dim](可选)[/dim]")
                if tool_name == "git":
                    console.print("    安装: https://git-scm.com/downloads")
                elif tool_name == "claude":
                    console.print("    安装: https://claude.ai/download")
                elif tool_name == "qwen":
                    console.print("    安装: Qwen Code 官方渠道")
            elif category == "shell":
                console.print(f"  [yellow]![/yellow] {tool_name} [dim](脚本环境)[/dim]")

        console.print()
    else:
        console.print("[green]OK - 所有工具都已可用![/green]")
        console.print()


def _print_check_json(result: dict) -> None:
    """
    以 JSON 格式输出工具检测结果

    Args:
        result: check_all_tools() 返回的结果
    """
    # 合并所有工具到一个列表
    all_tools = []

    for tool in result["required_tools"]:
        all_tools.append({**tool, "category": "required"})

    for tool in result["optional_tools"]:
        all_tools.append({**tool, "category": "optional"})

    all_tools.append({**result["shell"], "category": "shell"})

    # 输出 JSON
    output = {"status": "success", "tools": all_tools}

    console.print(json_module.dumps(output, indent=2, ensure_ascii=False))


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="显示版本信息"),
) -> None:
    """
    ElecSpeckit CLI 主入口

    可用选项:
    - --version / -v: 显示版本信息

    可用命令:
    - init: 初始化 ElecSpeckit 项目结构
    - check: 检查工具可用性
    """
    if version:
        from elecspeckit_init import __version__

        console.print(f"ElecSpeckit CLI 版本: {__version__}")
        return

    if ctx.invoked_subcommand is None:
        # 未提供任何命令,显示帮助信息
        console.print(app.info.help)
        console.print("\n[cyan]使用 --help 查看详细帮助信息[/cyan]")


if __name__ == "__main__":
    app()
