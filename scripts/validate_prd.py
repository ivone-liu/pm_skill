#!/usr/bin/env python3
"""Validate a PRD markdown file against the skill's structural checklist.

Usage:
  python scripts/validate_prd.py --input prd.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "一句话简介",
    "需求目标",
    "用户诉求",
    "业务诉求",
    "需求概述",
    "需求详述",
    "文档记录",
]

RECOMMENDED_SECTIONS = [
    "ROI",
    "名词解释",
    "竞品分析",
    "埋点方案",
    "验收标准",
    "边界情况",
    "异常",
]

DIAGRAM_HINTS = [
    "流程图",
    "泳道图",
    "状态机",
    "线框图",
    ".svg",
    "架构图",
]


def find_missing(content: str, labels: list[str]) -> list[str]:
    missing = []
    for label in labels:
        if not re.search(re.escape(label), content, re.IGNORECASE):
            missing.append(label)
    return missing


def count_headings(content: str) -> int:
    return len(re.findall(r"^(#|\d+\.)", content, flags=re.MULTILINE))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PRD markdown")
    parser.add_argument("--input", required=True, help="Path to markdown PRD")
    args = parser.parse_args()

    path = Path(args.input)
    content = path.read_text(encoding="utf-8")

    missing_required = find_missing(content, REQUIRED_SECTIONS)
    missing_recommended = find_missing(content, RECOMMENDED_SECTIONS)
    diagram_found = any(h in content for h in DIAGRAM_HINTS)
    heading_count = count_headings(content)

    print(f"FILE: {path}")
    print(f"HEADINGS: {heading_count}")
    print(f"REQUIRED_MISSING: {', '.join(missing_required) if missing_required else 'none'}")
    print(f"RECOMMENDED_MISSING: {', '.join(missing_recommended) if missing_recommended else 'none'}")
    print(f"DIAGRAM_REFERENCES: {'yes' if diagram_found else 'no'}")

    score = 100
    score -= len(missing_required) * 12
    score -= len(missing_recommended) * 4
    if not diagram_found:
        score -= 10
    if heading_count < 8:
        score -= 8
    score = max(0, score)
    print(f"QUALITY_SCORE: {score}")

    if missing_required:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
