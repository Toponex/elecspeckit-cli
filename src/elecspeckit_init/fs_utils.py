"""
文件系统工具函数

提供模板复制、目录创建和幂等检查的帮助函数
"""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class FileChange:
    """文件变更记录"""

    path: Path
    change_type: str  # "created", "updated", "backed_up", "skipped"
    backup_path: Optional[Path] = None
    message: str = ""


@dataclass
class ChangeSummary:
    """变更摘要"""

    changes: List[FileChange]
    total_created: int = 0
    total_updated: int = 0
    total_backed_up: int = 0
    total_skipped: int = 0

    def add_change(self, change: FileChange) -> None:
        """添加变更记录并更新计数"""
        self.changes.append(change)
        if change.change_type == "created":
            self.total_created += 1
        elif change.change_type == "updated":
            self.total_updated += 1
        elif change.change_type == "backed_up":
            self.total_backed_up += 1
        elif change.change_type == "skipped":
            self.total_skipped += 1


def ensure_directory_exists(path: Path) -> bool:
    """
    确保目录存在,如不存在则创建

    Args:
        path: 目录路径

    Returns:
        True 如果目录被创建,False 如果目录已存在

    Raises:
        PermissionError: 无写权限
        OSError: 其他文件系统错误
    """
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"路径 {path} 已存在但不是目录")
        return False

    path.mkdir(parents=True, exist_ok=True)
    return True


def write_or_update_file(
    target_path: Path, content: str, create_backup: bool = False, backup_suffix: str = ".bak"
) -> FileChange:
    """
    写入或更新文件,支持备份

    Args:
        target_path: 目标文件路径
        content: 文件内容
        create_backup: 是否为已存在文件创建备份
        backup_suffix: 备份文件后缀

    Returns:
        FileChange 对象记录变更信息

    Raises:
        PermissionError: 无写权限
        OSError: 磁盘空间不足等文件系统错误
    """
    # 确保父目录存在
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 检查文件是否已存在
    file_exists = target_path.exists()
    backup_path = None

    if file_exists:
        # 读取现有内容检查是否需要更新
        try:
            existing_content = target_path.read_text(encoding="utf-8")
            if existing_content == content:
                # 内容相同,跳过
                return FileChange(
                    path=target_path, change_type="skipped", message="内容相同,无需更新"
                )
        except Exception:
            # 无法读取现有文件,继续覆盖
            pass

        # 创建备份
        if create_backup:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = target_path.parent / f"{target_path.name}{backup_suffix}.{timestamp}"
            shutil.copy2(target_path, backup_path)

        # 写入新内容
        target_path.write_text(content, encoding="utf-8")

        return FileChange(
            path=target_path,
            change_type="backed_up" if create_backup else "updated",
            backup_path=backup_path,
            message="已更新" + (f" (备份: {backup_path.name})" if backup_path else ""),
        )
    else:
        # 创建新文件
        target_path.write_text(content, encoding="utf-8")

        return FileChange(path=target_path, change_type="created", message="已创建")


def copy_directory_tree(
    source_dir: Path, target_dir: Path, overwrite: bool = False, create_backup: bool = False
) -> ChangeSummary:
    """
    递归复制目录树

    Args:
        source_dir: 源目录
        target_dir: 目标目录
        overwrite: 是否覆盖已存在文件
        create_backup: 覆盖时是否创建备份

    Returns:
        ChangeSummary 包含所有文件变更记录

    Raises:
        FileNotFoundError: 源目录不存在
        PermissionError: 无写权限
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")

    if not source_dir.is_dir():
        raise ValueError(f"源路径不是目录: {source_dir}")

    summary = ChangeSummary(changes=[])

    # 递归遍历源目录
    for source_file in source_dir.rglob("*"):
        if source_file.is_file():
            # 计算相对路径
            relative_path = source_file.relative_to(source_dir)
            target_file = target_dir / relative_path

            # 读取源文件内容
            content = source_file.read_text(encoding="utf-8")

            # 检查是否需要跳过
            if target_file.exists() and not overwrite:
                change = FileChange(
                    path=target_file, change_type="skipped", message="文件已存在,跳过"
                )
            else:
                # 写入或更新文件
                change = write_or_update_file(target_file, content, create_backup=create_backup)

            summary.add_change(change)

    return summary


def is_empty_directory(path: Path) -> bool:
    """
    检查目录是否为空(允许 .git 等隐藏文件)

    Args:
        path: 目录路径

    Returns:
        True 如果目录为空或只包含 .git

    Raises:
        FileNotFoundError: 目录不存在
    """
    if not path.exists():
        raise FileNotFoundError(f"目录不存在: {path}")

    if not path.is_dir():
        raise ValueError(f"路径 {path} 不是目录")

    # 列出所有文件和目录,排除 .git
    items = [item for item in path.iterdir() if item.name != ".git"]
    return len(items) == 0


def is_elecspeckit_project(path: Path) -> bool:
    """
    检查目录是否为已有的 ElecSpeckit 项目

    Args:
        path: 目录路径

    Returns:
        True 如果目录包含 .elecspecify/ 和 (.claude/ 或 .qwen/)

    Raises:
        FileNotFoundError: 目录不存在
    """
    if not path.exists():
        raise FileNotFoundError(f"目录不存在: {path}")

    elecspecify_dir = path / ".elecspecify"
    claude_dir = path / ".claude"
    qwen_dir = path / ".qwen"

    # 必须有 .elecspecify/ 且至少有一个平台目录
    return elecspecify_dir.exists() and (claude_dir.exists() or qwen_dir.exists())
