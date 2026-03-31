# Clarifying Question Guide for PRD Work

This guide exists for one reason: a PRD generator should not pretend the upstream brief is complete when it is not.

## 1. First decide whether the gap matters

Ask follow-up questions only for information that changes one of these:
- solution direction
- target flow
- role / permission model
- platform-specific interaction
- implementation depth
- success criteria

If the gap does not change those, write the draft and mark the assumption.

## 2. What counts as blocking information

Typical blocking gaps:
- who the target user is
- what problem is being solved
- which platform this is for
- whether this is new design or modification of an existing flow
- whether the goal is review-level or engineering-level delivery
- whether there are hard constraints such as compliance, payment, permissions, or third-party dependencies

## 3. Good follow-up question structure

Each question should ideally contain three things:
1. the missing point
2. a narrow set of options or a precise answer format
3. why it matters

Template:
- [missing point]? [options if useful]. 这会直接影响 [design / scope / implementation].

Example:
- 这个功能面向的是普通用户、内部运营，还是管理员？这会直接影响页面入口、权限和操作范围。
- 你希望这版 PRD 更偏评审方案，还是直接给研发落地？这会决定我写到“功能层”还是“技术实现层”。

## 4. Recommended question buckets

### 4.1 User and scenario
- 谁在用
- 在什么场景下用
- 当前是首次使用、重复使用，还是异常处理场景

### 4.2 Platform and role
- Web / App / Mini Program / Backend
- single role or multiple roles
- whether permissions differ

### 4.3 Current state
- existing flow
- current pain point
- what is already in production
- what is being changed

### 4.4 Goal and success
- optimize what exactly
- business vs user goal
- success metric or qualitative review goal

### 4.5 Constraints
- time limit
- compliance
- integration with existing systems
- data source limitations
- performance expectations

## 5. Question count discipline

Do not dump twelve questions.

Use this rule:
- simple request: 0 to 3 questions
- medium request: 3 to 5 questions
- complex but incomplete request: 5 to 7 questions

If there are more than seven meaningful questions, the real problem is that the request is still at discovery stage. Say that plainly and switch to a discovery-first mode.

## 6. How to proceed when answers are incomplete

If the user answers only part of the questions:
- incorporate answered facts
- convert the rest into explicit assumptions
- list unresolved decisions in `待确认项`
- do not keep re-asking the same thing unless it blocks the core solution

## 7. Bad habits to avoid

- asking generic questions like “请补充更多信息”
- asking questions that the PRD can safely assume
- asking one question at a time when a grouped batch is possible
- writing a full PRD with fake certainty when core facts are missing
- replacing missing product thinking with long template text
