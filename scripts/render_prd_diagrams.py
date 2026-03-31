#!/usr/bin/env python3
"""Render common PRD diagrams to SVG from JSON specs.

Supported types:
- flowchart
- swimlane
- wireframe
- state-machine
- timeline
- architecture

Usage:
  python scripts/render_prd_diagrams.py --spec spec.json --out ./diagrams
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

FONT = "Arial, PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif"
PALETTE = {
    "bg": "#FFFFFF",
    "card": "#F8FAFC",
    "card_alt": "#F1F5F9",
    "line": "#CBD5E1",
    "text": "#0F172A",
    "muted": "#475569",
    "accent": "#2563EB",
    "accent_soft": "#DBEAFE",
    "danger": "#DC2626",
    "success": "#16A34A",
}


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class SVG:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.parts = []

    def add(self, s: str) -> None:
        self.parts.append(s)

    def start(self, title: str = "", subtitle: str = "") -> None:
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">')
        self.add('<defs><filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/></filter></defs>')
        self.rect(0, 0, self.width, self.height, fill=PALETTE["bg"], stroke=PALETTE["bg"], rx=0)
        if title:
            self.text(36, 40, title, 24, 700, PALETTE["text"])
        if subtitle:
            self.text(36, 66, subtitle, 13, 400, PALETTE["muted"])

    def finish(self) -> str:
        return "\n".join(self.parts + ["</svg>"])

    def text(self, x, y, text, size=14, weight=400, fill=None, anchor="start"):
        fill = fill or PALETTE["text"]
        self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(text)}</text>')

    def rect(self, x, y, w, h, fill=None, stroke=None, rx=14, sw=1.5, shadow=False):
        filter_attr = ' filter="url(#shadow)"' if shadow else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or PALETTE["card"]}" stroke="{stroke or PALETTE["line"]}" stroke-width="{sw}"{filter_attr} />')

    def line(self, x1, y1, x2, y2, stroke=None, sw=2.2):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke or PALETTE["accent"]}" stroke-width="{sw}" />')

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=2):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill or PALETTE["card"]}" stroke="{stroke or PALETTE["line"]}" stroke-width="{sw}" />')

    def polygon(self, points, fill=None, stroke=None, sw=1.5):
        self.add(f'<polygon points="{points}" fill="{fill or PALETTE["card"]}" stroke="{stroke or PALETTE["line"]}" stroke-width="{sw}" />')

    def arrow(self, x1, y1, x2, y2, label=None, stroke=None):
        stroke = stroke or PALETTE["accent"]
        self.line(x1, y1, x2, y2, stroke=stroke)
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 8
        p1 = (x2, y2)
        p2 = (x2 - size * math.cos(angle - math.pi / 6), y2 - size * math.sin(angle - math.pi / 6))
        p3 = (x2 - size * math.cos(angle + math.pi / 6), y2 - size * math.sin(angle + math.pi / 6))
        self.add(f'<polygon points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}" fill="{stroke}" />')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
            tw = max(20, len(str(label)) * 7 + 10)
            self.rect(mx - tw / 2, my - 12, tw, 24, fill="#FFFFFF", stroke="#E2E8F0", rx=8, sw=1)
            self.text(mx, my + 4, label, 12, 400, PALETTE["muted"], anchor="middle")


def box_size(label: str, min_w=150, h=70):
    return max(min_w, 28 + len(str(label)) * 14), h


def centered_text(svg: SVG, x, y, w, h, label, sub=None):
    svg.text(x + w / 2, y + h / 2 + (0 if not sub else -6), label, 14, 600, PALETTE["text"], anchor="middle")
    if sub:
        svg.text(x + 12, y + h / 2 + 18, sub, 11, 400, PALETTE["muted"])


def render_flowchart(d):
    nodes = d["nodes"]
    edges = d.get("edges", [])
    layout = d.get("layout", "horizontal")
    gap = 80
    margin_x, margin_y = 36, 96
    sizes = {n["id"]: box_size(n.get("label", n["id"])) for n in nodes}
    pos = {}
    x, y = margin_x, margin_y
    for n in nodes:
        w, h = sizes[n["id"]]
        pos[n["id"]] = (x, y, w, h)
        if layout == "horizontal":
            x += w + gap
        else:
            y += h + gap
    width = max(px + w for px, py, w, h in pos.values()) + margin_x
    height = max(py + h for px, py, w, h in pos.values()) + margin_y
    svg = SVG(width, height)
    svg.start(d.get("title", "流程图"), d.get("subtitle", "主流程图"))
    for n in nodes:
        x, y, w, h = pos[n["id"]]
        shape = n.get("shape", "rect")
        if shape == "diamond":
            pts = f"{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}"
            svg.polygon(pts, fill="#FFFFFF")
            svg.text(x + w/2, y + h/2 + 5, n.get("label", n["id"]), 14, 600, PALETTE["text"], anchor="middle")
        else:
            rx = 30 if shape == "terminal" else 14
            svg.rect(x, y, w, h, fill="#FFFFFF", rx=rx)
            centered_text(svg, x, y, w, h, n.get("label", n["id"]))
    for e in edges:
        fx, fy, fw, fh = pos[e["from"]]
        tx, ty, tw, th = pos[e["to"]]
        if layout == "horizontal":
            svg.arrow(fx + fw, fy + fh/2, tx, ty + th/2, e.get("label"), e.get("color"))
        else:
            svg.arrow(fx + fw/2, fy + fh, tx + tw/2, ty, e.get("label"), e.get("color"))
    return svg.finish()


def render_swimlane(d):
    lanes = d["lanes"]
    steps = d["steps"]
    edges = d.get("edges", [])
    lane_w = 250
    lane_h = max(234, 120 + 90 * max(1, math.ceil(len(steps) / max(1, len(lanes)))))
    margin_x, margin_y = 36, 96
    width = margin_x * 2 + lane_w * len(lanes) + 10 * (len(lanes) - 1)
    height = lane_h + 130
    svg = SVG(width, height)
    svg.start(d.get("title", "泳道图"), d.get("subtitle", "参与方与交互顺序"))
    lane_pos = {}
    for i, lane in enumerate(lanes):
        x = margin_x + i * (lane_w + 10)
        svg.rect(x, margin_y, lane_w, lane_h, fill=PALETTE["card_alt"], stroke="#E2E8F0", rx=16)
        svg.rect(x, margin_y, lane_w, 56, fill="#E2E8F0", stroke=PALETTE["line"], rx=16)
        svg.text(x + 18, margin_y + 34, lane, 15, 700)
        lane_pos[lane] = x
    step_pos = {}
    lane_counts = {lane: 0 for lane in lanes}
    for s in steps:
        lx = lane_pos[s["lane"]]
        idx = lane_counts[s["lane"]]
        lane_counts[s["lane"]] += 1
        x = lx + 16
        y = margin_y + 78 + idx * 98
        w, h = lane_w - 34, 80
        svg.rect(x, y, w, h, fill="#FFFFFF", stroke="#94A3B8")
        centered_text(svg, x, y, w, h, s.get("label", s["id"]))
        step_pos[s["id"]] = (x, y, w, h)
    for e in edges:
        fx, fy, fw, fh = step_pos[e["from"]]
        tx, ty, tw, th = step_pos[e["to"]]
        svg.arrow(fx + fw/2, fy + fh, tx + tw/2, ty, e.get("label"), e.get("color"))
    return svg.finish()


def render_wireframe(d):
    title = d.get("title", "页面线框图")
    subtitle = d.get("subtitle", "页面结构示意")
    phone_w, phone_h = 250, 470
    margin_x, margin_y = 36, 100
    width, height = 322, 620
    svg = SVG(width, height)
    svg.start(title, subtitle)
    svg.rect(margin_x, margin_y, phone_w, phone_h, fill="#FFFFFF", stroke="#94A3B8", rx=24)
    blocks = d.get("blocks", [])
    if not blocks:
        blocks = [
            {"title": "标题区", "note": "页面标题与操作"},
            {"title": "基本信息区", "note": "字段/状态/负责人"},
            {"title": "需求说明", "note": "问题、目标、范围"},
            {"title": "流程与附件", "note": "流程图/原型/附件"},
            {"title": "评论与记录", "note": "评审意见/变更记录"},
        ]
    x = margin_x + 16
    y = margin_y + 16
    for i, b in enumerate(blocks):
        bh = 42 if i == 0 else (72 if i == 1 else 88)
        if i == len(blocks) - 1:
            bh = 110
        svg.rect(x, y, phone_w - 32, bh, fill=PALETTE["card"], stroke=PALETTE["line"], rx=14)
        svg.text(x + 12, y + 26, b["title"], 13 if i else 15, 700 if i == 0 else 600)
        if b.get("note"):
            svg.text(x + 12, y + 46 if i else y + 26, b["note"], 11, 400, PALETTE["muted"])
        y += bh + 14
    if d.get("footer_button", "提交评审"):
        svg.rect(x, 498, phone_w - 32, 44, fill=PALETTE["accent_soft"], stroke="#93C5FD", rx=14)
        svg.text(margin_x + phone_w / 2, 526, d.get("footer_button", "提交评审"), 13, 700, anchor="middle")
    return svg.finish()


def render_state_machine(d):
    states = d["states"]
    edges = d.get("edges", [])
    radius = 42
    gap = 170
    margin_x, margin_y = 80, 140
    width = margin_x * 2 + gap * max(1, len(states) - 1) + radius * 2
    height = 320
    svg = SVG(width, height)
    svg.start(d.get("title", "状态机图"), d.get("subtitle", "状态变化与允许动作"))
    pos = {}
    for i, s in enumerate(states):
        x = margin_x + i * gap
        y = margin_y
        pos[s["id"]] = (x, y)
        fill = PALETTE["card"]
        stroke = PALETTE["line"]
        if s.get("kind") == "start":
            fill, stroke = PALETTE["accent_soft"], PALETTE["accent"]
        elif s.get("kind") == "end":
            fill, stroke = "#FEE2E2", PALETTE["danger"]
        svg.circle(x, y, radius, fill=fill, stroke=stroke)
        svg.text(x, y + 6, s.get("label", s["id"]), 13, 700, anchor="middle")
    for e in edges:
        x1, y1 = pos[e["from"]]
        x2, y2 = pos[e["to"]]
        svg.arrow(x1 + radius, y1, x2 - radius, y2, e.get("label"), e.get("color"))
    return svg.finish()


def render_timeline(d):
    phases = d["phases"]
    margin_x, y = 46, 180
    width = margin_x * 2 + 220 * len(phases)
    height = 320
    svg = SVG(width, height)
    svg.start(d.get("title", "项目时间线"), d.get("subtitle", "里程碑与交付节奏"))
    svg.line(margin_x, y, width - margin_x, y, stroke="#94A3B8", sw=4)
    for i, p in enumerate(phases):
        x = margin_x + 110 + i * 220
        svg.circle(x, y, 16, fill=PALETTE["accent_soft"], stroke=PALETTE["accent"], sw=3)
        svg.text(x, y - 36, p.get("title", f"阶段{i+1}"), 15, 700, anchor="middle")
        svg.text(x, y + 46, p.get("date", ""), 13, 400, PALETTE["muted"], anchor="middle")
        if p.get("milestone"):
            svg.rect(x - 78, y + 62, 156, 56, fill="#FFFFFF", stroke=PALETTE["line"], rx=12)
            svg.text(x, y + 95, p["milestone"], 12, 400, anchor="middle")
    return svg.finish()


def render_architecture(d):
    nodes = d["nodes"]
    edges = d.get("edges", [])
    cols = max(2, min(4, d.get("cols", 3)))
    margin_x, margin_y = 46, 110
    gap_x, gap_y = 54, 70
    pos = {}
    max_w, h = 180, 88
    for i, n in enumerate(nodes):
        row, col = divmod(i, cols)
        x = margin_x + col * (max_w + gap_x)
        y = margin_y + row * (h + gap_y)
        pos[n["id"]] = (x, y, max_w, h)
    width = max(x + w for x, y, w, h in pos.values()) + margin_x
    height = max(y + h for x, y, w, h in pos.values()) + margin_y
    svg = SVG(width, height)
    svg.start(d.get("title", "系统架构图"), d.get("subtitle", "模块关系与数据流"))
    for n in nodes:
        x, y, w, h = pos[n["id"]]
        svg.rect(x, y, w, h, fill=n.get("fill", PALETTE["card"]), stroke=n.get("stroke", PALETTE["line"]), rx=18)
        centered_text(svg, x, y, w, h, n.get("label", n["id"]), n.get("note"))
    for e in edges:
        fx, fy, fw, fh = pos[e["from"]]
        tx, ty, tw, th = pos[e["to"]]
        svg.arrow(fx + fw/2, fy + fh, tx + tw/2, ty, e.get("label"), e.get("color"))
    return svg.finish()


RENDERERS = {
    "flowchart": render_flowchart,
    "swimlane": render_swimlane,
    "wireframe": render_wireframe,
    "state-machine": render_state_machine,
    "timeline": render_timeline,
    "architecture": render_architecture,
}


def render(spec: dict, out_dir: Path):
    diagrams = spec.get("diagrams") or [spec]
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for i, d in enumerate(diagrams, start=1):
        dtype = d.get("type")
        if dtype not in RENDERERS:
            raise ValueError(f"unsupported diagram type: {dtype}")
        filename = d.get("filename") or f"diagram-{i}.svg"
        svg = RENDERERS[dtype](d)
        path = out_dir / filename
        path.write_text(svg, encoding="utf-8")
        written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PRD diagrams to SVG")
    parser.add_argument("--spec", required=True, help="Path to JSON spec file")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    paths = render(spec, Path(args.out))
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
