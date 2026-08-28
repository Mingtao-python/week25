# 📘 Coding Style & Engineering Standards
> **Author**: Mingtao  
> **Version**: 1.0 (Based on Week25 Review)  
> **Philosophy**: "Theory must match Implementation. Reports must reflect Reality."

---

## 1. Core Principles (核心原则)

### 1.1 Single Source of Truth (唯一事实来源)
- **禁止**在 README、代码常量、文档中维护多套不一致的定义（如 Event Schema）。
- **必须**建立中央配置文件（如 `event_schema.py`），所有模块统一 `import`。
- **示例**:
  ```python
  # ❌ Bad: Hardcoded in multiple files
  ALLOWED_EVENTS = {"app_open", "question_submitted"} # in logger.py
  # README says: "help_button_clicked" is allowed -> INCONSISTENCY

  # ✅ Good: Centralized
  # schema.py
  ALLOWED_EVENTS = {"app_open", "help_button_clicked", ...}
  # logger.py & app.py
  from schema import ALLOWED_EVENTS
  ```

### 1.2 Instrumentation vs. Specification (真实埋点 vs. 打印说明)
- **禁止**只写 `print()` 函数来模拟用户流程。
- **必须**将埋点代码 (`log_event`) 嵌入真实的业务逻辑触发点（UI 点击、API 响应）。
- **标准**: 用户操作 -> 触发业务逻辑 -> 自动记录事件。

### 1.3 Data Integrity & Security (数据完整性与安全)
- **禁止**盲目信任输入数据。
- **必须**实施以下基础校验：
  1. **Schema Validation**: 字段类型、必填项检查。
  2. **Duplicate Detection**: 基于 `session_id + event_name + timestamp/id` 去重。
  3. **Sequence Validation**: 拒绝不可能的序列（如未 `plan_created` 直接 `plan_completed`）。
  4. **Bounds Checking**: 数值不能为负，完成率不能超过 100%。

---

## 2. Algorithm Logic Standards (算法逻辑标准)

### 2.1 Funnel Analysis (漏斗分析)
- **错误逻辑**: 仅检查事件是否在 Session 中“出现过” (Set existence)。
- **正确逻辑**: 必须检查**时间顺序** (Temporal Sequence)。
  - Step N 必须在 Step N-1 **之后**发生。
  - 如果顺序颠倒，视为漏斗断裂。
- **实现**:
  ```python
  events.sort(key=lambda e: e["timestamp"])
  current_step_index = 0
  for event in events:
      if event.name == funnel[current_step_index]:
          current_step_index += 1
  ```

### 2.2 A/B Testing (A/B 测试)
- **输入校验**:
  - `exposed < 0` or `completed < 0` -> Raise `ValueError`
  - `completed > exposed` -> Raise `ValueError` (转化率不能 > 100%)
  - `len(variants) < 2` -> Raise `ValueError` (必须至少两组)
- **输出**: 必须包含置信度或显著性说明（若样本小，标记为 "Exploratory"）。

---

## 3. Documentation & Reporting (文档与报告)

### 3.1 Testing Report (测试报告)
- **禁止**声称 "PASS" 如果代码未实际覆盖该逻辑。
- **必须包含**的课程要求测试用例：
  1. **Malformed Input**: 缺少字段、类型错误。
  2. **Duplicate Events**: 同一事件重复提交。
  3. **Impossible Sequences**: 逻辑冲突的事件流。
  4. **Edge Cases**: 空数据、极大值、极小值。
- **格式**: `Assertion` 必须对应代码中的实际 `if/raise` 逻辑。

### 3.2 User Stories & Feedback (用户故事与反馈)
- **User Stories**: 必须包含 `As a... I want... So that...` 格式及明确的 `Acceptance Criteria`。
- **Feedback Mechanism**: 产品中必须包含真实的反馈入口（如 👍/👎 按钮），而非仅理论描述。
- **User Testing**: 
  - 必须有真实用户或受监督的模拟测试 (Supervised Simulation)。
  - 记录：Task, Completion Status, Time, Confusion Points, Comments.
  - **Before/After Evidence**: 必须展示改进前后的数据对比（即使样本小）。

---

## 4. Project Structure (推荐结构)

```text
weekXX/
├── app/                # 真实可运行的 MVP (Flask/Streamlit/React)
│   ├── main.py
│   └── templates/
├── analytics/          # 核心分析逻辑
│   ├── schema.py       # ⭐ 唯一事实来源
│   ├── logger.py
│   ├── funnel.py
│   └── ab_test.py
├── tests/              # 自动化测试
│   └── test_all.py
├── docs/               # 学术交付物
│   ├── user_stories.md
│   ├── user_testing_report.md
│   └── improvement_plan.md
├── CODING_STYLE_GUIDE.md # 本文件
└── README.md
```

---

## 5. Pre-Commit Checklist (提交前自查)

在 `git commit` 之前，必须确认：
- [ ] **Schema Consistency**: README 中的事件定义与 `schema.py` 完全一致吗？
- [ ] **Real Instrumentation**: 事件是用户触发的，还是脚本打印的？
- [ ] **Logic Validation**: 漏斗是否检查了顺序？A/B 是否检查了边界？
- [ ] **Security**: 是否处理了重复数据和非法序列？
- [ ] **Test Coverage**: 测试报告中的 "PASS" 都有对应的 `assert` 代码支持吗？
- [ ] **User Evidence**: 是否有真实的用户测试记录和改进证据？

---

> "Perfect is the enemy of good, but **inconsistency** is the enemy of engineering."
> — Mingtao's Engineering Law
