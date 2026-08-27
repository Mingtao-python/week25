# Week25 — AI Learning Platform V2

**Bootcamp V2.0 — Week 25 Engineering & Academic Product Deliverables**

**Student:** Mingtao  
**Date:** 2026-08-22

---

## Quick Start

### Run Engineering Tests
```bash
cd week25
python tests/test_all.py
```

### Run Event Logger Demo
```bash
cd week25
python analytics/event_logger.py
```

### Run Funnel Analyzer
```bash
cd week25
python analytics/funnel_analyzer.py
```

### Run A/B Analyzer Demo
```bash
cd week25
python analytics/ab_analyzer.py
```

### Launch MVP Web App
```bash
cd week25
pip install flask
python app/mvp_app.py
# Open http://localhost:5000 in browser
```

---

## Project Structure

```
week25/
├── app/
│   └── mvp_app.py              # Flask MVP with real event instrumentation
├── analytics/
│   ├── event_schema.py         # Centralized event schema (single source of truth)
│   ├── event_logger.py         # Event logging with validation, dedup, sequence checks
│   ├── funnel_analyzer.py      # Funnel analysis with sequence validation
│   └── ab_analyzer.py          # A/B testing with input validation
├── feedback/                   # (Reserved for future feedback collection)
├── tests/
│   └── test_all.py             # Comprehensive test suite
├── docs/
│   ├── user_stories.md         # User stories, flow, feedback, A/B plan, testing report
│   ├── testing_report.md       # Detailed engineering test results
│   └── user_flow.md            # User flow documentation
└── README.md                   # This file
```

---

## Week25 Requirements Checklist

### Engineering Assignment ✅

| Requirement | File | Status |
|-------------|------|--------|
| Event Logger | `analytics/event_logger.py` | ✅ Complete |
| Funnel Analyzer | `analytics/funnel_analyzer.py` | ✅ Complete |
| A/B Analyzer | `analytics/ab_analyzer.py` | ✅ Complete |
| User Flow Instrumentation | `app/mvp_app.py` | ✅ Complete |
| Testing Report | `docs/testing_report.md` | ✅ Complete |

### Academic Product ✅

| Requirement | File | Status |
|-------------|------|--------|
| Target User + Core Problem | `docs/user_stories.md` §1 | ✅ Complete |
| End-to-End Core Flow | `docs/user_stories.md` §2 | ✅ Complete |
| 3+ User Stories | `docs/user_stories.md` §3 | ✅ Complete |
| Event Instrumentation | `docs/user_stories.md` §4 | ✅ Complete |
| Feedback Mechanism | `docs/user_stories.md` §5 | ✅ Complete |
| A/B Test Plan | `docs/user_stories.md` §6 | ✅ Complete |
| User Testing Report | `docs/user_stories.md` §7 | ✅ Complete |
| Security/Privacy Notes | `docs/user_stories.md` §8 | ✅ Complete |
| Mobile-First Usability | `docs/user_stories.md` §9 | ✅ Complete |
| Before/After Evidence | `docs/user_stories.md` §10 | ✅ Complete |

---

## Key Improvements Over Original Submission

### 1. Centralized Event Schema ✅
**Problem:** README, logger, and flow each maintained separate event lists  
**Solution:** Single `event_schema.py` imported by all modules

### 2. Proper Funnel Sequence Validation ✅
**Problem:** Original code only checked if events existed, not order  
**Solution:** Events sorted by timestamp, steps validated in sequence

### 3. Duplicate Event Detection ✅
**Problem:** No deduplication  
**Solution:** Unique key (session_id + event_name + timestamp) prevents duplicates

### 4. Impossible Sequence Detection ✅
**Problem:** `helpful_marked` could occur without `answer_received`  
**Solution:** Sequence rules enforce logical event order

### 5. A/B Input Validation ✅
**Problem:** Could produce 150% conversion rates  
**Solution:** Validates completed ≤ exposed, no negatives, ≥2 variants

### 6. Real Product Instrumentation ✅
**Problem:** Events were just printed, not triggered by user actions  
**Solution:** Flask app logs events on actual user interactions

### 7. Comprehensive Testing ✅
**Problem:** Missing duplicate event tests, incorrect funnel tests  
**Solution:** 8 automated tests covering all edge cases

---

## Core User Flow (Instrumented)

```
1. Open App → app_open
2. Tap "Ask Question" → help_button_clicked
3. Form Shown → question_input_shown
4. Submit Question → question_submitted
5. Receive Answer → answer_received
6. Mark Feedback → helpful_marked OR feedback_submitted
7. Continue Learning → continue_learning_clicked
```

All events are logged to `events.log` with session tracking.

---

## Event Schema

Allowed events (defined in `analytics/event_schema.py`):

```python
ALLOWED_EVENTS = {
    "app_open",
    "help_button_clicked",
    "question_input_shown",
    "question_submitted",
    "answer_received",
    "helpful_marked",
    "continue_learning_clicked",
    "feedback_submitted",
    "session_end",
    "plan_created",
    "plan_completed",
}
```

Required fields: `event_name`, `timestamp`, `session_id`  
Optional fields: `variant`, `properties`

---

## Security Features

1. **Schema Validation** — All events validated before logging
2. **Duplicate Detection** — Same event can't be logged twice
3. **Sequence Validation** — Impossible sequences rejected
4. **Data Minimization** — Only anonymous session IDs stored
5. **Input Sanitization** — Type checking on all fields

---

## Test Results

```
Total Tests: 8
Passed: 8
Failed: 0

🎉 ALL TESTS PASSED!

Week25 Engineering components validated:
- Event Logger: Schema validation ✓, Duplicate detection ✓, Impossible sequence ✓
- Funnel Analyzer: Sequence validation ✓, Missing step handling ✓
- A/B Analyzer: Input validation ✓, Edge cases ✓, Correct calculations ✓
```

---

## User Testing Summary

| Tester | Role | Completed | Time | Feedback |
|--------|------|-----------|------|----------|
| Tester 1 | Student (Grade 10) | ✅ | 45 sec | "Very easy to use" |
| Tester 2 | Parent | ✅ | 60 sec | "Would like history feature" |

**Top 3 Improvements:**
1. Add question history
2. Add subject tags
3. Add share feature

---

## Next Steps

1. Recruit 10+ real users for larger-scale testing
2. Connect to real AI API for actual answers
3. Implement A/B test with live traffic
4. Build teacher dashboard for analytics

---

## License

Educational project for Bootcamp V2.0 Week 25.
