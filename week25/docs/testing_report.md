# Week25 Engineering — Comprehensive Testing Report

**Student:** Mingtao  
**Date:** 2026-08-22  
**Bootcamp V2.0 — Week 25**

---

## Executive Summary

All Week25 engineering components have been tested and validated:

| Component | Tests Run | Passed | Failed | Status |
|-----------|-----------|--------|--------|--------|
| Event Logger | 2 | 2 | 0 | ✅ PASS |
| Funnel Analyzer | 2 | 2 | 0 | ✅ PASS |
| A/B Analyzer | 4 | 4 | 0 | ✅ PASS |
| **Total** | **8** | **8** | **0** | **✅ ALL PASS** |

---

## 1. Event Logger Tests (`analytics/event_logger.py`)

### 1.1 Duplicate Event Detection ✅

**Test Case:** Log the same event twice (same session_id + event_name + timestamp)

**Input:**
```python
event1 = {"event_name": "app_open", "timestamp": 1000.0, "session_id": "test_sess"}
event2 = {"event_name": "app_open", "timestamp": 1000.0, "session_id": "test_sess"}  # Duplicate
```

**Expected Result:** First event logged, second rejected with "duplicate" message

**Actual Result:**
```
First event: Logged event: app_open
Duplicate event: Rejected duplicate event
```

**Status:** ✅ PASS

---

### 1.2 Impossible Sequence Detection ✅

**Test Case A:** `helpful_marked` without prior `answer_received`

**Input:**
```python
event = {"event_name": "helpful_marked", "timestamp": 2000.0, "session_id": "new_session"}
```

**Expected Result:** Rejected with sequence error

**Actual Result:**
```
Impossible sequence: helpful_marked without prior answer_received
```

**Test Case B:** `answer_received` without prior `question_submitted`

**Input:**
```python
event = {"event_name": "answer_received", "timestamp": 3000.0, "session_id": "another_session"}
```

**Expected Result:** Rejected with sequence error

**Actual Result:**
```
Impossible sequence: answer_received without prior question_submitted
```

**Status:** ✅ PASS

---

## 2. Funnel Analyzer Tests (`analytics/funnel_analyzer.py`)

### 2.1 Funnel Sequence Validation ✅

**Test Case:** Events arrive out of order (`helpful_marked` before `answer_received`)

**Input:**
```python
[
    {"event_name": "app_open", "timestamp": 1.0, "session_id": "seq_test"},
    {"event_name": "question_submitted", "timestamp": 2.0, "session_id": "seq_test"},
    {"event_name": "helpful_marked", "timestamp": 3.0, "session_id": "seq_test"},  # Out of order!
    {"event_name": "answer_received", "timestamp": 4.0, "session_id": "seq_test"},
]
```

**Expected Result:** 
- Events sorted by timestamp
- Funnel processes in order: app_open → question_submitted → (skip helpful_marked) → answer_received
- Funnel NOT completed because helpful_marked was seen before answer_received

**Actual Result:**
```
Events in order: ['app_open', 'question_submitted', 'answer_received']
Max step reached: 2
Funnel completed: False
```

**Status:** ✅ PASS

---

### 2.2 Missing Step Detection ✅

**Test Case:** `answer_received` is completely missing

**Input:**
```python
[
    {"event_name": "app_open", "timestamp": 1.0, "session_id": "missing_test"},
    {"event_name": "question_submitted", "timestamp": 2.0, "session_id": "missing_test"},
    {"event_name": "helpful_marked", "timestamp": 3.0, "session_id": "missing_test"},
]
```

**Expected Result:** 
- Only app_open and question_submitted counted
- answer_received = False
- helpful_marked = False (wrong order)

**Actual Result:**
```
Events in order: ['app_open', 'question_submitted']
Step reached - answer_received: False
Step reached - helpful_marked: False
```

**Status:** ✅ PASS

---

## 3. A/B Analyzer Tests (`analytics/ab_analyzer.py`)

### 3.1 Invalid Data: completed > exposed ✅

**Input:**
```python
[
    {"name": "A", "exposed": 40, "completed": 50},  # Invalid!
    {"name": "B", "exposed": 42, "completed": 25},
]
```

**Expected Result:** Rejected with error mentioning both fields

**Actual Result:**
```
'completed' (50) > 'exposed' (40) for variant A
```

**Status:** ✅ PASS

---

### 3.2 Invalid Data: Negative Values ✅

**Input:**
```python
[
    {"name": "A", "exposed": -10, "completed": 5},  # Invalid!
    {"name": "B", "exposed": 42, "completed": 25},
]
```

**Expected Result:** Rejected with "negative" error

**Actual Result:**
```
'exposed' cannot be negative for variant A: -10
```

**Status:** ✅ PASS

---

### 3.3 Invalid Data: Single Variant ✅

**Input:**
```python
[{"name": "A", "exposed": 40, "completed": 18}]
```

**Expected Result:** Rejected, needs at least 2 variants

**Actual Result:**
```
A/B test requires at least 2 variants
```

**Status:** ✅ PASS

---

### 3.4 Valid A/B Analysis ✅

**Input:**
```python
[
    {"name": "A", "exposed": 40, "completed": 18},
    {"name": "B", "exposed": 42, "completed": 25},
]
```

**Expected Result:**
- A conversion: 18/40 = 0.45
- B conversion: 25/42 ≈ 0.595
- Difference: ≈ 0.145

**Actual Result:**
```
Variant A conversion: 0.4500
Variant B conversion: 0.5952
Difference B-A: 0.1452
```

**Status:** ✅ PASS

---

## 4. Additional Tests Performed

### 4.1 Schema Validation (Event Logger)
- ✅ Rejects invalid event names
- ✅ Rejects missing required fields
- ✅ Rejects wrong field types

### 4.2 Edge Cases (A/B Analyzer)
- ✅ Zero exposed users (returns 0.0 conversion)
- ✅ Small sample warning (< 100 users)

### 4.3 Mobile-First UI (MVP App)
- ✅ Responsive layout tested on mobile viewport
- ✅ Touch targets ≥ 48px
- ✅ Text size ≥ 16px

---

## 5. Test Coverage Summary

| Requirement | Covered By | Status |
|-------------|------------|--------|
| Duplicate event detection | test_event_logger_duplicate_detection | ✅ |
| Malformed input rejection | Event schema validation | ✅ |
| Impossible sequence rejection | test_event_logger_impossible_sequence | ✅ |
| Funnel sequence validation | test_funnel_sequence_validation | ✅ |
| Missing step handling | test_funnel_missing_answer_received | ✅ |
| A/B input validation | test_ab_validation_* | ✅ |
| Correct A/B calculations | test_ab_valid_analysis | ✅ |
| Small sample warning | Built into ab_analyzer | ✅ |

---

## 6. How to Run Tests

```bash
cd week25
python tests/test_all.py
```

Expected output:
```
🎉 ALL TESTS PASSED!

Week25 Engineering components validated:
- Event Logger: Schema validation ✓, Duplicate detection ✓, Impossible sequence ✓
- Funnel Analyzer: Sequence validation ✓, Missing step handling ✓
- A/B Analyzer: Input validation ✓, Edge cases ✓, Correct calculations ✓
```

---

## 7. Conclusion

All Week25 Engineering Assignment requirements have been met:

1. ✅ **Event Logger** — Schema validation, duplicate detection, impossible sequence detection
2. ✅ **Funnel Analyzer** — Proper sequence validation, correct drop-off calculation
3. ✅ **A/B Analyzer** — Input validation, edge case handling, correct calculations
4. ✅ **Testing Report** — Comprehensive tests with pass/fail evidence
5. ✅ **User Flow Instrumentation** — Real events tied to actual user actions in MVP app

This project demonstrates evidence-based engineering with automated testing, proper input validation, and data integrity checks as required by Week25.
