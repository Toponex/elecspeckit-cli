"""
跨平台处理工具

实现 FR-045, FR-046: 处理平台特定的路径、编码和权限
- Windows: 路径使用反斜杠、GBK 编码处理
- Linux/macOS: 路径使用正斜杠、UTF-8 编码、POSIX 权限
"""

import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Optional


def get_platform() -> str:
    """
    获取当前平台标识

    Returns:
        'windows', 'linux', 或 'macos'
    """
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Darwin':
        return 'macos'
    elif system == 'Linux':
        return 'linux'
    else:
        return system.lower()


def setup_utf8_output():
    """
    FR-045: 设置 UTF-8 输出，解决 Windows GBK 编码问题

    在 Windows GBK 环境下，强制使用 UTF-8 编码输出中文字符
    """
    if sys.platform == 'win32':
        import io
        # 重新配置 stdout/stderr 使用 UTF-8
        if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def normalize_path(path: str | Path) -> Path:
    """
    FR-046: 规范化路径为当前平台的格式

    Args:
        path: 原始路径（字符串或 Path 对象）

    Returns:
        规范化后的 Path 对象
    """
    path = Path(path)

    # 在 Windows 上，确保使用反斜杠
    if get_platform() == 'windows':
        return Path(str(path).replace('/', '\\'))

    # 在 POSIX 系统上，确保使用正斜杠
    return Path(str(path).replace('\\', '/'))


def set_file_permissions(file_path: str | Path, mode: int = 0o600):
    """
    FR-046: 设置文件权限（仅 POSIX 系统）

    Args:
        file_path: 文件路径
        mode: 权限模式（默认 0o600，仅所有者可读写）

    Note:
        Windows 上此函数不执行任何操作（Windows 使用 ACL 而非 POSIX 权限）
    """
    if get_platform() in ['linux', 'macos']:
        try:
            os.chmod(file_path, mode)
        except OSError as e:
            print(f"警告: 无法设置文件权限 {file_path}: {e}", file=sys.stderr)


def read_text_file(file_path: str | Path, encoding: str = 'utf-8') -> str:
    """
    FR-045: 读取文本文件，强制使用 UTF-8 编码

    Args:
        file_path: 文件路径
        encoding: 编码格式（默认 utf-8）

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 编码错误
    """
    path = Path(file_path)

    try:
        return path.read_text(encoding=encoding)
    except UnicodeDecodeError as e:
        # 在 Windows GBK 环境下可能需要回退到 GBK
        if get_platform() == 'windows' and encoding == 'utf-8':
            try:
                return path.read_text(encoding='gbk')
            except UnicodeDecodeError:
                raise e  # 重新抛出原始错误
        raise


def write_text_file(file_path: str | Path, content: str, encoding: str = 'utf-8', set_permissions: bool = True):
    """
    FR-045, FR-046: 写入文本文件，强制使用 UTF-8 编码并设置权限

    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 编码格式（默认 utf-8）
        set_permissions: 是否设置文件权限（POSIX 系统）

    Raises:
        PermissionError: 权限不足
        OSError: 写入失败
    """
    path = Path(file_path)

    # 确保父目录存在
    path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    path.write_text(content, encoding=encoding)

    # 设置权限（仅 POSIX 系统）
    if set_permissions:
        set_file_permissions(path, mode=0o600)


def check_disk_space(path: str | Path, required_mb: int = 100) -> tuple[bool, int]:
    """
    FR-047: 检查磁盘剩余空间

    Args:
        path: 检查路径（通常是项目根目录）
        required_mb: 需要的最小空间（MB）

    Returns:
        (是否足够, 实际剩余空间MB)
    """
    path = Path(path)

    try:
        stat = shutil.disk_usage(path)
        free_mb = stat.free // (1024 * 1024)

        return free_mb >= required_mb, free_mb
    except OSError as e:
        print(f"警告: 无法检查磁盘空间: {e}", file=sys.stderr)
        return True, 0  # 无法检查时假设足够


def check_python_dependency(package: str, min_version: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """
    FR-048: 检查 Python 依赖库是否安装

    Args:
        package: 包名（如 'arxiv', 'requests'）
        min_version: 最小版本号（可选，如 '2.31.0'）

    Returns:
        (是否已安装, 当前版本号)
    """
    try:
        import importlib.metadata

        try:
            version = importlib.metadata.version(package)

            # 检查版本号
            if min_version:
                from packaging import version as pkg_version
                if pkg_version.parse(version) < pkg_version.parse(min_version):
                    return False, version

            return True, version
        except importlib.metadata.PackageNotFoundError:
            return False, None
    except ImportError:
        # Python < 3.8，使用 pkg_resources
        try:
            import pkg_resources

            try:
                version = pkg_resources.get_distribution(package).version

                # 检查版本号
                if min_version:
                    from packaging import version as pkg_version
                    if pkg_version.parse(version) < pkg_version.parse(min_version):
                        return False, version

                return True, version
            except pkg_resources.DistributionNotFound:
                return False, None
        except ImportError:
            # 无法检查依赖
            return True, None  # 假设已安装


def get_install_command(package: str, version: Optional[str] = None) -> str:
    """
    生成依赖安装命令

    Args:
        package: 包名
        version: 版本号（可选）

    Returns:
        安装命令字符串
    """
    if version:
        return f"uv pip install {package}>={version}"
    return f"uv pip install {package}"


# 依赖库映射（FR-048）
SKILL_DEPENDENCIES = {
    'arxiv-search': [('arxiv', '2.0.0')],
    'perplexity-search': [('requests', '2.31.0'), ('litellm', '1.0.0')],
    'openalex-database': [('pyalex', '0.13')],
    'mouser-component-search': [('requests', '2.31.0')],
}


def check_skill_dependencies(skill_name: str) -> list[str]:
    """
    检查 Skill 的依赖库

    Args:
        skill_name: Skill 名称

    Returns:
        缺失依赖的错误消息列表
    """
    errors = []

    dependencies = SKILL_DEPENDENCIES.get(skill_name, [])

    for package, min_version in dependencies:
        installed, current_version = check_python_dependency(package, min_version)

        if not installed:
            if current_version:
                # 版本过低
                errors.append(
                    f"缺少依赖库 {package}（当前版本 {current_version} < {min_version}），"
                    f"请运行 '{get_install_command(package, min_version)}' 升级"
                )
            else:
                # 未安装
                errors.append(
                    f"缺少依赖库 {package}，请运行 '{get_install_command(package, min_version)}' 安装"
                )

    return errors


def create_backup_directory(base_path: str | Path, name: str = "backup") -> Path:
    """
    FR-053: 创建带时间戳的备份目录

    Args:
        base_path: 基础路径（如 .elecspecify）
        name: 备份目录名称（默认 'backup'）

    Returns:
        备份目录路径（如 .elecspecify/backup/claude.bak.20251217-143022）
    """
    from datetime import datetime

    base_path = Path(base_path)
    backup_root = base_path / name

    # 创建备份根目录
    backup_root.mkdir(parents=True, exist_ok=True)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # 创建带时间戳的备份目录
    backup_dir = backup_root / f"claude.bak.{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    return backup_dir


def safe_copy_tree(src: str | Path, dst: str | Path, create_backup: bool = True):
    """
    安全复制目录树，可选创建备份

    Args:
        src: 源目录
        dst: 目标目录
        create_backup: 如果目标已存在，是否创建备份

    Returns:
        备份目录路径（如果创建了备份），否则 None
    """
    src = Path(src)
    dst = Path(dst)

    backup_path = None

    # 如果目标已存在且需要备份
    if dst.exists() and create_backup:
        # 检测是否包含用户自定义内容（简单检查：是否有非模板文件）
        has_custom_content = any(
            f.name not in ['commands', 'templates', 'scripts', 'skills']
            for f in dst.iterdir()
            if f.is_dir()
        )

        if has_custom_content:
            # 创建备份
            backup_root = dst.parent.parent / '.elecspecify' / 'backup'
            backup_path = create_backup_directory(backup_root.parent, 'backup')

            # 复制到备份目录
            shutil.copytree(dst, backup_path / dst.name)
            print(f"已备份现有配置到: {backup_path}")

    # 复制目录树
    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    return backup_path
