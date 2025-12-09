"""
Git 工具模块

处理 Git 仓库初始化和提交
"""

import subprocess
from pathlib import Path
from typing import Optional, Tuple


def is_git_available() -> bool:
    """
    检查 git 命令是否可用

    Returns:
        True 如果 git 可用,否则 False
    """
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def is_git_repo(base_dir: Path) -> bool:
    """
    检查目录是否已经是 git 仓库

    Args:
        base_dir: 要检查的目录

    Returns:
        True 如果是 git 仓库,否则 False
    """
    git_dir = base_dir / ".git"
    return git_dir.exists() and git_dir.is_dir()


def initialize_git_repo(
    base_dir: Path, initial_commit_message: Optional[str] = None
) -> Tuple[bool, str]:
    """
    初始化 git 仓库并创建初始提交

    Args:
        base_dir: 项目根目录
        initial_commit_message: 初始提交消息

    Returns:
        (成功标志, 消息) 元组
    """
    # 检查 git 是否可用
    if not is_git_available():
        return False, "git 命令不可用,跳过 git 初始化"

    # 检查是否已经是 git 仓库
    if is_git_repo(base_dir):
        return False, "目录已经是 git 仓库,跳过 git 初始化"

    try:
        # 执行 git init
        result = subprocess.run(
            ["git", "init"], cwd=base_dir, capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            return False, f"git init 失败: {result.stderr}"

        # 添加所有文件
        subprocess.run(
            ["git", "add", "."], cwd=base_dir, capture_output=True, text=True, timeout=10
        )

        # 创建初始提交
        commit_msg = initial_commit_message or "Initial ElecSpeckit project setup"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return True, "git 仓库已初始化 (未创建提交)"

        return True, "git 仓库已初始化并创建初始提交"

    except subprocess.TimeoutExpired:
        return False, "git 操作超时"
    except Exception as e:
        return False, f"git 初始化失败: {e}"


def get_git_status(base_dir: Path) -> Optional[str]:
    """
    获取 git 状态

    Args:
        base_dir: 项目根目录

    Returns:
        git status 输出,如果失败则返回 None
    """
    if not is_git_repo(base_dir):
        return None

    try:
        result = subprocess.run(
            ["git", "status", "--short"], cwd=base_dir, capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return None


# 别名，用于向后兼容和测试
init_git_repo = initialize_git_repo
check_git_available = is_git_available
git_available = is_git_available
check_git_repo = is_git_repo
is_git_repository = is_git_repo
auto_init_git = initialize_git_repo
