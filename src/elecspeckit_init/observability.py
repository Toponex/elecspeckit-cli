"""
可观测性工具模块

提供 Skills 部署进度跟踪功能，使用 rich 库进行可视化展示
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID


class DeploymentStep(Enum):
    """部署步骤枚举"""

    VALIDATING_SOURCE = "validating_source"
    COPYING_FILES = "copying_files"
    DEPLOYING_SKILL = "deploying_skill"
    GENERATING_CONFIG = "generating_config"
    COMPLETED = "completed"

    def description(self) -> str:
        """返回步骤的中文描述"""
        descriptions = {
            DeploymentStep.VALIDATING_SOURCE: "验证源 Skills 库完整性",
            DeploymentStep.COPYING_FILES: "复制 Skills 文件",
            DeploymentStep.DEPLOYING_SKILL: "部署 Skill",
            DeploymentStep.GENERATING_CONFIG: "生成 skill_config.json",
            DeploymentStep.COMPLETED: "部署完成",
        }
        return descriptions.get(self, "未知步骤")


@dataclass
class SkillsDeploymentTracker:
    """
    Skills 部署进度跟踪器 (T008)

    使用 rich 库可视化展示 Skills 部署进度，支持：
    - 总体进度跟踪
    - 单个 Skill 部署状态
    - 失败记录
    - 部署耗时统计

    Examples:
        >>> tracker = SkillsDeploymentTracker(total_skills=23)
        >>> tracker.start()
        >>> tracker.set_step(DeploymentStep.VALIDATING_SOURCE)
        >>> tracker.start_skill("hardware-design", "硬件设计 Skill")
        >>> tracker.complete_skill("hardware-design")
        >>> summary = tracker.get_summary()
        >>> tracker.finish()
    """

    total_skills: int
    completed_skills: int = 0
    failed_skills: int = 0
    current_step: Optional[DeploymentStep] = None
    current_skill_name: Optional[str] = None
    failures: Dict[str, str] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    _progress: Optional[Progress] = None
    _task_id: Optional[TaskID] = None
    _console: Console = field(default_factory=Console)

    def __post_init__(self):
        """初始化控制台和进度条"""
        if self.start_time is None:
            self.start_time = datetime.now()

    def start(self):
        """开始进度跟踪（初始化 rich Progress 对象）"""
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self._console,
        )
        self._progress.start()
        self._task_id = self._progress.add_task(
            f"部署 {self.total_skills} 个 Skills", total=self.total_skills
        )

    def finish(self):
        """完成进度跟踪（停止 rich Progress）"""
        if self._progress:
            self._progress.stop()
        self.end_time = datetime.now()

    def set_step(self, step: DeploymentStep):
        """
        设置当前部署步骤

        Args:
            step: 部署步骤枚举值
        """
        self.current_step = step

        if self._progress and self._task_id is not None:
            # 更新进度条描述
            if step == DeploymentStep.DEPLOYING_SKILL and self.current_skill_name:
                description = f"部署 Skill: {self.current_skill_name}"
            else:
                description = step.description()

            self._progress.update(self._task_id, description=description)

    def start_skill(self, skill_name: str, description: str):
        """
        开始部署单个 Skill

        Args:
            skill_name: Skill 名称（如 "hardware-design"）
            description: Skill 描述（如 "硬件设计 Skill"）
        """
        self.current_skill_name = skill_name
        self.set_step(DeploymentStep.DEPLOYING_SKILL)

    def complete_skill(self, skill_name: str):
        """
        完成单个 Skill 部署

        Args:
            skill_name: Skill 名称

        Raises:
            ValueError: 当前未在部署该 Skill 时
        """
        if self.current_skill_name != skill_name:
            raise ValueError(f"未找到正在部署的 Skill: {skill_name}")

        self.completed_skills += 1
        self.current_skill_name = None

        if self._progress and self._task_id is not None:
            self._progress.update(self._task_id, completed=self.completed_skills)

    def fail_skill(self, skill_name: str, error_message: str):
        """
        记录 Skill 部署失败

        Args:
            skill_name: Skill 名称
            error_message: 错误信息
        """
        self.failed_skills += 1
        self.failures[skill_name] = error_message
        self.current_skill_name = None

        if self._progress and self._task_id is not None:
            # 失败的 Skill 也算作已处理
            self._progress.update(
                self._task_id, completed=self.completed_skills + self.failed_skills
            )

    @property
    def progress_percentage(self) -> float:
        """
        计算当前进度百分比

        Returns:
            进度百分比（0.0 - 100.0）
        """
        if self.total_skills == 0:
            return 0.0
        return (self.completed_skills / self.total_skills) * 100.0

    def get_summary(self) -> Dict:
        """
        生成部署摘要

        Returns:
            包含总数、已完成、失败、成功率、耗时的字典
        """
        elapsed_seconds = 0.0
        if self.start_time:
            end = self.end_time if self.end_time else datetime.now()
            elapsed_seconds = (end - self.start_time).total_seconds()

        success_rate = 0.0
        if self.total_skills > 0:
            success_rate = (self.completed_skills / self.total_skills) * 100.0

        return {
            "total": self.total_skills,
            "completed": self.completed_skills,
            "failed": self.failed_skills,
            "success_rate": success_rate,
            "elapsed_seconds": elapsed_seconds,
            "failures": dict(self.failures),
        }

    def print_summary(self):
        """打印部署摘要（使用 rich 格式化输出）"""
        summary = self.get_summary()

        self._console.print("\n[bold green]部署摘要[/bold green]")
        self._console.print(f"总 Skills 数: {summary['total']}")
        self._console.print(f"成功部署: {summary['completed']}")
        self._console.print(f"失败: {summary['failed']}")
        self._console.print(f"成功率: {summary['success_rate']:.1f}%")
        self._console.print(f"耗时: {summary['elapsed_seconds']:.2f} 秒")

        if summary["failures"]:
            self._console.print("\n[bold red]失败的 Skills:[/bold red]")
            for skill_name, error in summary["failures"].items():
                self._console.print(f"  - {skill_name}: {error}")
