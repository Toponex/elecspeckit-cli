"""
交互式用户界面组件

提供基于 readchar 和 Rich 的交互式选择界面
"""

from dataclasses import dataclass
from typing import List, Optional

try:
    import readchar

    READCHAR_AVAILABLE = True
except ImportError:
    READCHAR_AVAILABLE = False

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


@dataclass
class SelectOption:
    """选择选项"""

    value: str
    label: str
    description: str = ""


class InteractiveSelector:
    """
    交互式选择器

    使用 readchar 监听键盘输入 (↑/↓选择, Enter确认, Esc取消)
    使用 Rich 渲染选择界面 (带高亮的选项列表)
    """

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def select_platform(self, title: str = "选择 AI 平台") -> Optional[str]:
        """
        平台选择界面

        Args:
            title: 选择界面标题

        Returns:
            选择的平台 ("claude" 或 "qwen"),如果取消则返回 None
        """
        options = [
            SelectOption(
                value="claude",
                label="Claude Code",
                description="Anthropic Claude AI 驱动的代码助手平台",
            ),
            SelectOption(
                value="qwen", label="Qwen Code", description="通义千问 AI 驱动的代码助手平台"
            ),
        ]

        return self._select_single(title, options)

    def _select_single(self, title: str, options: List[SelectOption]) -> Optional[str]:
        """
        单选选择器核心实现

        Args:
            title: 选择界面标题
            options: 选项列表

        Returns:
            选择的选项值,如果取消则返回 None
        """
        if not READCHAR_AVAILABLE:
            # 降级到简单文本输入模式
            return self._select_single_fallback(title, options)

        current_index = 0

        # 隐藏光标
        self.console.show_cursor(False)

        try:
            while True:
                # 清屏并渲染选择界面
                self.console.clear()
                self._render_selection(title, options, current_index)

                # 读取键盘输入
                key = readchar.readkey()

                if key == readchar.key.UP:
                    # 上箭头 - 向上移动
                    current_index = (current_index - 1) % len(options)

                elif key == readchar.key.DOWN:
                    # 下箭头 - 向下移动
                    current_index = (current_index + 1) % len(options)

                elif key == readchar.key.ENTER or key == "\r" or key == "\n":
                    # Enter - 确认选择
                    self.console.clear()
                    return options[current_index].value

                elif key == readchar.key.ESC:
                    # Esc - 取消
                    self.console.clear()
                    return None

        finally:
            # 恢复光标
            self.console.show_cursor(True)

    def _render_selection(
        self, title: str, options: List[SelectOption], current_index: int
    ) -> None:
        """
        渲染选择界面

        Args:
            title: 标题
            options: 选项列表
            current_index: 当前选中的索引
        """
        # 创建选项表格
        table = Table(show_header=False, show_edge=False, box=None, padding=(0, 2))
        table.add_column("Indicator", width=3)
        table.add_column("Option")
        table.add_column("Description")

        for i, option in enumerate(options):
            indicator = "►" if i == current_index else " "

            # 高亮当前选项
            if i == current_index:
                label_style = "bold cyan"
                desc_style = "cyan"
            else:
                label_style = "white"
                desc_style = "dim"

            table.add_row(
                f"[{label_style}]{indicator}[/{label_style}]",
                f"[{label_style}]{option.label}[/{label_style}]",
                f"[{desc_style}]{option.description}[/{desc_style}]",
            )

        # 创建面板
        panel = Panel(
            table,
            title=f"[bold]{title}[/bold]",
            subtitle="[dim]↑/↓ 选择  Enter 确认  Esc 取消[/dim]",
            border_style="blue",
            box=box.ROUNDED,
        )

        self.console.print(panel)

    def _select_single_fallback(self, title: str, options: List[SelectOption]) -> Optional[str]:
        """
        降级模式 - 使用简单文本输入

        当 readchar 不可用时使用此方法
        """
        self.console.print(f"\n[bold cyan]{title}[/bold cyan]\n")

        for i, option in enumerate(options, start=1):
            self.console.print(f"  {i}. [bold]{option.label}[/bold] - {option.description}")

        while True:
            try:
                choice = input(f"\n请选择 (1-{len(options)}) 或按 Enter 取消: ").strip()

                if not choice:
                    return None

                index = int(choice) - 1
                if 0 <= index < len(options):
                    return options[index].value
                else:
                    self.console.print("[yellow]无效选择,请重试[/yellow]")

            except ValueError:
                self.console.print("[yellow]请输入有效数字[/yellow]")
            except KeyboardInterrupt:
                return None


def confirm_action(message: str, console: Optional[Console] = None) -> bool:
    """
    确认操作

    Args:
        message: 确认消息
        console: Rich Console 实例

    Returns:
        True 如果用户确认,否则 False
    """
    console = console or Console()

    try:
        response = input(f"{message} [y/N]: ").strip().lower()
        return response in ("y", "yes", "是")
    except KeyboardInterrupt:
        return False
