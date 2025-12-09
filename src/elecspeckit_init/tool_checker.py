"""
工具可用性检测模块

提供工具检测、版本提取、平台判断等功能
"""

import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def check_tool(tool_name: str) -> Dict[str, any]:
    """
    检测单个工具的可用性

    Args:
        tool_name: 工具名称（如 'git', 'uv', 'claude'）

    Returns:
        工具信息字典，包含：
        - tool: 工具名称
        - available: 是否可用
        - version: 版本号（如果可用）
        - path: 完整路径（如果可用）
    """
    tool_path = shutil.which(tool_name)

    if tool_path is None:
        return {"tool": tool_name, "available": False, "version": None, "path": None}

    # 尝试获取版本信息
    version = _extract_version_from_tool(tool_name, tool_path)

    return {"tool": tool_name, "available": True, "version": version, "path": tool_path}


def check_tools(tool_names: List[str]) -> List[Dict[str, any]]:
    """
    批量检测多个工具的可用性

    Args:
        tool_names: 工具名称列表

    Returns:
        工具信息列表
    """
    return [check_tool(tool) for tool in tool_names]


def check_shell() -> Dict[str, any]:
    """
    检测当前平台的 Shell 可用性

    Returns:
        Shell 信息字典
    """
    current_platform = platform.system()

    if current_platform == "Windows":
        # Windows: 优先检测 pwsh，其次 powershell
        for shell in ["pwsh", "powershell"]:
            result = check_tool(shell)
            if result["available"]:
                return result

        # 都不可用，返回 pwsh 作为默认
        return check_tool("pwsh")

    else:
        # Unix-like: 检测 bash
        # 注意：bash 通常在 /bin/bash，可能不在 PATH 中
        bash_result = check_tool("bash")

        if not bash_result["available"]:
            # 尝试 /bin/bash
            bash_path = Path("/bin/bash")
            if bash_path.exists():
                version = _extract_version_from_path("bash", str(bash_path))
                return {
                    "tool": "bash",
                    "available": True,
                    "version": version,
                    "path": str(bash_path),
                }

        return bash_result


def _extract_version_from_tool(tool_name: str, tool_path: str) -> Optional[str]:
    """
    从工具执行 --version 命令提取版本号

    Args:
        tool_name: 工具名称
        tool_path: 工具完整路径

    Returns:
        版本号字符串，或 None
    """
    return _extract_version_from_path(tool_name, tool_path)


def _extract_version_from_path(tool_name: str, tool_path: str) -> Optional[str]:
    """
    从工具路径执行 --version 并提取版本号

    Args:
        tool_name: 工具名称
        tool_path: 工具完整路径

    Returns:
        版本号字符串，或 None
    """
    try:
        # 尝试执行 --version
        result = subprocess.run([tool_path, "--version"], capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            return extract_version(result.stdout)

    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass

    return None


def extract_version(version_output: str) -> Optional[str]:
    """
    从版本输出中提取版本号

    支持多种版本输出格式:
    - "git version 2.43.0"
    - "Python 3.11.5"
    - "uv 0.5.0"
    - "claude 1.2.3"

    Args:
        version_output: --version 命令的输出

    Returns:
        版本号字符串（如 "2.43.0"），或 None
    """
    if not version_output:
        return None

    # 尝试多个版本号模式
    patterns = [
        r"version\s+([0-9]+\.[0-9]+\.[0-9]+)",  # "version 2.43.0"
        r"([0-9]+\.[0-9]+\.[0-9]+)",  # "2.43.0"
        r"v([0-9]+\.[0-9]+\.[0-9]+)",  # "v2.43.0"
        r"([0-9]+\.[0-9]+)",  # "2.43"
    ]

    for pattern in patterns:
        match = re.search(pattern, version_output, re.IGNORECASE)
        if match:
            return match.group(1) if "version" in pattern or "v" in pattern else match.group(0)

    return None


def get_platform_name() -> str:
    """
    获取当前平台名称

    Returns:
        平台名称: 'Windows', 'Linux', 'Darwin' (macOS)
    """
    return platform.system()


def get_required_tools() -> List[str]:
    """
    获取必需工具列表

    Returns:
        必需工具名称列表
    """
    return ["uv"]


def get_optional_tools() -> List[str]:
    """
    获取可选工具列表

    Returns:
        可选工具名称列表
    """
    return ["git", "claude", "qwen"]


def check_all_tools() -> Dict[str, any]:
    """
    检测所有工具（必需 + 可选 + Shell）

    Returns:
        包含所有工具检测结果的字典:
        - required_tools: 必需工具列表
        - optional_tools: 可选工具列表
        - shell: Shell 信息
    """
    required_tools = get_required_tools()
    optional_tools = get_optional_tools()

    return {
        "required_tools": check_tools(required_tools),
        "optional_tools": check_tools(optional_tools),
        "shell": check_shell(),
    }
