#!/usr/bin/env python3
"""
ElecSpeckit 占位脚本：kbconfig_update.py

约定职责（需求层面）：
- 作为 /elecspeckit.kbconfig 的后端脚本之一，根据由 Agent 生成的结构化 patch 更新
  `.elecspecify/memory/knowledge-sources.json` 的内容，支持在 `standards`、`company_kb`、
  `reference_designs`、`web.sources` 四个类别下增加/修改/删除“多条”信息源条目；
- 在应用变更时保持文件的基本结构（四个顶层类别 + web 策略字段），避免因 LLM 幻觉
  直接重写整文件导致格式损坏；
- 支持从命令行传入一个 JSON patch 文件路径，例如：

    python .elecspecify/scripts/kbconfig_update.py --patch .elecspecify/memory/kb_patch.json

当前版本仅作为占位实现，为了安全起见**不会实际修改 knowledge-sources.json**，而是：
- 校验 patch 文件是否存在；
- 将 patch 内容与目标文件路径打印到 stdout；
- 提示工程师在目标项目中按上述契约补充实际更新逻辑。
"""

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="ElecSpeckit kbconfig_update 占位脚本")
    parser.add_argument(
        "--patch",
        required=True,
        help="包含知识源配置变更的 JSON patch 文件路径",
    )
    parser.add_argument(
        "--kb",
        default=".elecspecify/memory/knowledge-sources.json",
        help="知识源配置文件路径（默认 .elecspecify/memory/knowledge-sources.json）",
    )
    args = parser.parse_args()

    patch_path = Path(args.patch)
    kb_path = Path(args.kb)

    if not patch_path.exists():
        print(f"[kbconfig_update] patch 文件不存在: {patch_path}", file=sys.stderr)
        sys.exit(1)

    if not kb_path.exists():
        print(f"[kbconfig_update] 知识源配置文件不存在: {kb_path}", file=sys.stderr)
        sys.exit(1)

    print("[kbconfig_update] 占位脚本，仅打印将要应用的变更，不修改实际文件。")
    print(f"[kbconfig_update] 目标配置文件: {kb_path}")
    print(f"[kbconfig_update] patch 文件: {patch_path}")
    print(
        "[kbconfig_update] 请在目标项目中实现实际的 patch 应用逻辑，"
        "并确保遵守项目宪法与 knowledge-sources.json 的结构约定。"
    )


if __name__ == "__main__":
    main()
