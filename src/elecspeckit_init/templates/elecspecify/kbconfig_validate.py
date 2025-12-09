#!/usr/bin/env python3
"""
ElecSpeckit 占位脚本：kbconfig_validate.py

约定职责（需求层面）：
- 对 `.elecspecify/memory/knowledge-sources.json` 进行只读检查，判断配置是否满足最小结构要求；
- 输出简单的 JSON 结果，供 /elecspeckit.constitution 等命令作为门禁使用，例如：

    { "status": "ok" }
    或
    { "status": "invalid", "reasons": ["missing section: web", "web.default_size out of range"] }

当前版本仅作为占位实现，为了安全起见不会解析文件结构，而是：
- 检查文件是否存在且非空；
- 在存在时输出 { "status": "ok" }；
- 不存在或为空时输出 { "status": "invalid", "reasons": [...] }。
"""

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="ElecSpeckit kbconfig_validate 占位脚本")
    parser.add_argument(
        "--kb",
        default=".elecspecify/memory/knowledge-sources.json",
        help="知识源配置文件路径（默认 .elecspecify/memory/knowledge-sources.json）",
    )
    args = parser.parse_args()

    kb_path = Path(args.kb)

    if not kb_path.exists():
        result = {
            "status": "invalid",
            "reasons": ["knowledge-sources file does not exist"],
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    raw = kb_path.read_text(encoding="utf-8").strip()
    if not raw:
        result = {
            "status": "invalid",
            "reasons": ["knowledge-sources file is empty"],
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        result = {
            "status": "invalid",
            "reasons": [f"knowledge-sources.json is not valid JSON: {exc}"],
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    reasons = []

    # 顶层类别检查
    for key in ("standards", "company_kb", "reference_designs", "web"):
        if key not in data:
            reasons.append(f"missing top-level section: {key}")

    # enabled/sources 一致性检查：enabled 为 true 时必须至少有一个 source
    for key in ("standards", "company_kb", "reference_designs"):
        section = data.get(key, {})
        enabled = bool(section.get("enabled"))
        sources = section.get("sources")
        if enabled and (not isinstance(sources, list) or not sources):
            reasons.append(f"{key}.enabled is true but {key}.sources is empty or not a list")

    web = data.get("web", {})
    web_enabled = bool(web.get("enabled"))
    web_sources = web.get("sources")
    if web_enabled and (not isinstance(web_sources, list) or not web_sources):
        reasons.append("web.enabled is true but web.sources is empty or not a list")

    if reasons:
        result = {"status": "invalid", "reasons": reasons}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    result = {"status": "ok"}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
