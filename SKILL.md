---
name: prd-writing-with-diagrams
description: Writes high-quality PRDs and draws the diagrams inside them. Use when the user asks to 写PRD, 写产品需求文档, 整理需求方案, 输出需求评审稿, 补充交互流程图, 绘制泳道图, 绘制状态机, 画线框图, 输出 markdown/docx/pdf PRD, or turn scattered notes into a structured requirement document with visuals.
license: MIT
compatibility: Designed for Claude.ai, Claude Code, and API environments with code execution. Uses bundled Python scripts to validate PRD structure and render SVG diagrams without external network access.
metadata:
  author: OpenAI
  version: 1.0.0
  category: product-management
  tags:
    - prd
    - product-requirements
    - diagrams
    - wireframes
    - documentation
---

# PRD Writing with Diagrams

This skill writes product requirement documents that are readable by product, design, engineering, QA, and operations. It also draws the diagrams that belong inside a PRD, instead of leaving the document visually hollow.

Follow this skill when the user wants a PRD,需求方案,需求评审稿,功能说明书,功能拆解文档,交互流转图,泳道图,状态机图,页面线框图,信息架构图,里程碑图, or a structured document from messy notes.

## Outcome

Produce a deliverable PRD with four layers:

1. **需求背景**: why this exists.
2. **需求概述**: a one-glance view of the whole thing.
3. **需求详述**: module-by-module execution details.
4. **配图与校验**: diagrams rendered as SVG plus a structural validation pass.

## Non-negotiable principles

1. **Do not use a rigid template blindly.** Pick the structure according to complexity, stakeholders, and delivery speed.
2. **One sentence first.** State why, how, and expected effect in plain language.
3. **Facts before adjectives.** Use user evidence, business logic, data, assumptions, risks, and edge cases.
4. **The PRD is for multiple readers.** Design for product, design, engineering, QA, operations, and future maintainers.
5. **If a picture reduces ambiguity, draw it.** Do not say “see design later” when the flow can already be expressed.
6. **If details are missing, make the minimum explicit assumptions and label them.** Do not stall on every ambiguity.

## When to ask follow-up questions

Ask only when the missing information blocks the core decision. Otherwise proceed with labeled assumptions.

Good reasons to ask:
- target users are unknown
- the main business goal is unclear
- the platform is unknown and changes the flow materially
- the current state or existing constraints are critical

If enough information exists, write the PRD directly.

## Standard workflow

### Step 1: Determine PRD mode

Classify the request into one of these modes:

- **MVP PRD**: fast, lean, core path first
- **Standard PRD**: complete document for review and implementation
- **Complex system PRD**: includes cross-role flow, state changes, backend logic, permissions, and milestones
- **Revision PRD**: modifies an existing flow and clearly marks changed sections

Then decide whether the document needs:
- user flow
- wireframe
- swimlane
- state machine
- architecture diagram
- timeline / milestones

Consult `references/prd-writing-principles.md` and `references/diagram-playbook.md` if the request is broad or complex.

### Step 2: Extract the minimum input frame

Before writing, capture these fields in working notes:

- feature / project name
- one-sentence summary
- target users
- user problem
- business goal
- current state
- scope in / out
- platforms and roles
- dependencies and constraints
- launch or review expectation
- metrics / success definition

If the user did not provide all of them, infer carefully and mark assumptions.

### Step 3: Build the document skeleton

Use this order unless the request strongly suggests another one:

1. 文档信息
2. 一句话简介
3. 需求背景
4. 需求目标
5. 用户诉求
6. 业务诉求
7. ROI / 优先级判断
8. 名词解释
9. 需求概述
10. 需求详述
11. 埋点方案
12. 验收标准
13. 风险 / 待确认项
14. 文档记录

For small urgent requests, compress the structure but do not lose clarity.

### Step 4: Write the PRD itself

Use the template in `assets/prd-template.md`.

#### 4.1 一句话简介

Write one plain sentence with three parts:
- why
- how
- expected effect

Bad:
- 提升用户体验
- 优化业务效率

Good:
- 为了降低新用户首次使用的决策成本，在首页增加场景化入口与默认推荐，预期提升首日核心行为转化率。

#### 4.2 需求背景

Include only what helps readers understand the demand:
- problem origin
- current pain points
- evidence
- why now
- related assumptions or constraints

#### 4.3 需求目标

Prefer measurable or at least falsifiable targets. Distinguish:
- user-facing objective
- business objective
- guardrails

#### 4.4 用户诉求 / 业务诉求

Separate them. Do not hide business goals under fake user value.

#### 4.5 需求概述

This section must make the whole demand understandable in under one minute.

Use diagrams when needed:
- **flowchart** for main user path and branching
- **wireframe** for a complex page structure
- **swimlane** for multi-role or multi-system collaboration
- **state-machine** for status changes
- **architecture** for module relations or data flow
- **timeline** for rollout / milestone planning

#### 4.6 需求详述

Write by module, journey, or dependency chain. Choose the order that is easiest to implement.

For each module, include:
- 模块概述
- 出现条件 / 进入条件 / 上级页面
- 页面元素 / 组件
- 交互规则
- 状态变化
- 文案规则
- 前端逻辑
- 后端逻辑
- 权限与角色差异
- 异常与边界情况
- 埋点
- 验收标准

When a module is complex, use bullets or tables. When a table reduces readability, use structured prose instead.

### Step 5: Draw the diagrams

If the PRD needs diagrams, create a JSON spec and render SVGs with the bundled script.

Command:

```bash
python scripts/render_prd_diagrams.py --spec /tmp/prd-diagrams.json --out /tmp/prd-diagrams
```

Use these diagram types:

- `flowchart`
- `wireframe`
- `swimlane`
- `state-machine`
- `timeline`
- `architecture`

Example spec patterns are in `assets/specs/`.

#### Diagram style rules

- Prefer clarity over decoration.
- Use Chinese labels matching the PRD terminology.
- Keep one diagram focused on one question.
- Do not cram exception flows into the main flow unless they are essential.
- Keep names consistent with the glossary and requirement text.

### Step 6: Validate before finalizing

Run:

```bash
python scripts/validate_prd.py --input prd.md
```

If validation reports missing required sections, fix the PRD before returning it.

### Step 7: Return deliverables

The final output should include:
- the PRD itself in markdown by default
- SVG diagrams when applicable
- a short assumption list when information was inferred
- unresolved questions only if they materially affect implementation

If the environment supports richer files, you may also export docx or pdf after the markdown is complete.

## Writing rules

### Use this tone

- plain
- concrete
- implementation-friendly
- no slogan filler
- no vague praise of the idea

### Use this level of detail

Enough for engineering and QA to start work without guessing the main logic.

### Avoid these common failures

- “提升体验” with no mechanism
- only describing happy path
- mixing user goal and business goal into one sentence
- pages listed with no state logic
- backend only named, not described
- diagrams mentioned but not drawn
- inconsistent naming between sections and figures
- dumping all content into a giant table

## Diagram generation examples

### Example A: User flow

```json
{
  "diagrams": [
    {
      "filename": "main-user-flow.svg",
      "type": "flowchart",
      "title": "新用户首登主流程",
      "layout": "horizontal",
      "nodes": [
        {"id": "home", "label": "首页"},
        {"id": "guide", "label": "引导弹层"},
        {"id": "task", "label": "完成首个任务"},
        {"id": "done", "label": "结果页", "shape": "terminal"}
      ],
      "edges": [
        {"from": "home", "to": "guide", "label": "首次进入"},
        {"from": "guide", "to": "task", "label": "继续"},
        {"from": "task", "to": "done", "label": "成功"}
      ]
    }
  ]
}
```

### Example B: Swimlane

```json
{
  "diagrams": [
    {
      "filename": "approval-swimlane.svg",
      "type": "swimlane",
      "title": "审核协作泳道图",
      "lanes": ["用户", "系统", "审核员"],
      "steps": [
        {"id": "s1", "lane": "用户", "label": "提交资料"},
        {"id": "s2", "lane": "系统", "label": "基础校验"},
        {"id": "s3", "lane": "审核员", "label": "人工审核"}
      ],
      "edges": [
        {"from": "s1", "to": "s2", "label": "提交后"},
        {"from": "s2", "to": "s3", "label": "校验通过"}
      ]
    }
  ]
}
```

## Troubleshooting

### Problem: The PRD is readable but still empty

Cause:
- too much abstract language
- no evidence or examples
- no exception flow

Fix:
- add user evidence
- add edge cases
- add state transitions or validation logic

### Problem: The document is long but engineering still cannot start

Cause:
- structure exists, execution logic missing

Fix:
- rewrite each module with explicit conditions, actions, status, errors, and acceptance rules

### Problem: Too many diagrams

Cause:
- drawing everything instead of answering the real ambiguity

Fix:
- keep only the diagrams that reduce disagreement

### Problem: Diagram labels conflict with the PRD text

Fix:
- standardize the glossary first
- regenerate diagrams after renaming terms

## References bundled with this skill

- `references/prd-writing-principles.md`
- `references/diagram-playbook.md`
- `references/quality-checklist.md`
- `references/example-prompts.md`
- `assets/prd-template.md`
- `assets/specs/*.json`

## Default execution pattern

When the user asks for a PRD and does not specify format:

1. write the PRD in markdown
2. generate SVG diagrams if the flow or structure is non-trivial
3. validate the markdown with the validation script
4. return the markdown plus the diagram files

Do not stop at “here is a structure suggestion” unless the user explicitly asked for a framework only.
