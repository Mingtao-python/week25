# Week25_Engineering — Testing Report
Bootcamp V2.0 — Week 25  
Student: Mingtao  
Date: 2026-08-22

This report documents all engineering tests performed for Week25, including:
- Event Logger validation
- Funnel Analyzer correctness
- A/B Analyzer correctness
- User Flow Instrumentation completeness
- Invalid input handling
- Data integrity & security checks

---

# 1. Event Logger Tests (`event_logger.py`)

## 1.1 Valid Event Test
**Input**

``` json
{
  "event_name": "app_open",
  "timestamp": 1787329685.67,
  "session_id": "sess_1",
  "variant": "A",
  "properties": {"device": "mobile"}
}
```


Expected Result  
Event is logged to events.log.

Actual Result  
Logged event: app_open

Status  
PASS

## 1.2 Invalid Event Name
Input:

```json
{
  "event_name": "unknown_event",
  "timestamp": 1787329685.67,
  "session_id": "sess_2",
  "properties": {}
}
``` 
Expected Result  
Event rejected.

Actual Result  
Rejected invalid event: {...}

Status  
PASS

## 1.3 Missing Timestamp
Input:
```json
{
  "event_name": "app_open",
  "session_id": "sess_3"
}
```
Expected Result  
Rejected.

Actual Result  
Rejected.

Status  
PASS

## 1.4 Wrong Type (timestamp as string)
Input: 
```json
{
  "event_name": "app_open",
  "timestamp": "not_a_number",
  "session_id": "sess_4"
}
```
Expected Result  
Rejected.

Actual Result  
Rejected.

Status  
PASS

1.5 Security Test — Unexpected Properties Type
Input: 

```json
{
  "event_name": "app_open",
  "timestamp": 1787329685.67,
  "session_id": "sess_5",
  "properties": "should_be_object"
}
```
Expected Result  
Rejected.

Actual Result  
Rejected.

Status  
PASS

# 2. Funnel Analyzer Tests (funnel_analyzer.py)
## 2.1 Complete Funnel Session
Events:

```
app_open
question_submitted
answer_received
helpful_marked
Expected Result
```

All steps conversion = 1.00  
No drop-off  
Actual Result:  

```
Total sessions: 1
app_open → 1.00
question_submitted → 1.00
answer_received → 1.00
helpful_marked → 1.00
```
Status  
PASS

## 2.2 Missing Step (answer_received)
Events:
```
app_open
question_submitted
helpful_marked
Expected Result
```

Drop-off at answer_received

helpful_marked should not count as valid completion

Actual Result:
```
Correct drop-off detected.
```

Status  
PASS

## 2.3 Multiple Sessions
Input:
- Two sessions, one complete, one partial.
- Expected Result
- Funnel counts per session
- Correct conversion per step

Actual Result: 
Matches expected.

Status  
PASS

# 3. A/B Analyzer Tests (ab_analyzer.py)
## 3.1 Provided Dataset
A = 40 exposed / 18 completed
B = 42 exposed / 25 completed

Expected Conversion

A = 0.45

B = 0.60

Difference = 0.15

Actual Output

```
Variant A: conversion=0.45
Variant B: conversion=0.60
Difference B - A: 0.15
```

Note: small sample → exploratory only  
Status  
PASS  

# 3.2 Zero Exposed (edge case)
Input:
```
A: exposed=0, completed=0
Expected Result
Conversion = 0.0
```
No crash.

Actual Result: 
Correct.

Status  
PASS

# 4. User Flow Instrumentation Tests (user_flow_instrumentation.py)
## 4.1 Flow Completeness
Expected:
- 8-step mobile-first flow
- Includes model call
- Includes permission check
- Includes retry path
- Includes success state

Actual: 
Flow printed correctly.

Status  
PASS

## 4.2 Event Coverage
Expected: 
- At least 6 events.

Actual: 
8 events printed:
```
app_open
help_button_clicked
question_input_shown
question_submitted
answer_received
helpful_marked
continue_learning_clicked
session_end
```
Status  
PASS

# 5. Data Integrity & Security Tests
# 5.1 Invalid Event Rejection
All malformed events rejected as expected.

Status  
PASS

# 5.2 No Personal Data Logged
Checked events.log:

- Only anonymous session IDs
- No names
- No prompts
- No sensitive content

Status  
PASS

## 5.3 Event Schema Enforcement
All required fields validated.

Status  
PASS

# 6. Summary & Conclusion
Module	Result
Event Logger	PASS
Funnel Analyzer	PASS
A/B Analyzer	PASS
User Flow Instrumentation	PASS
Data Security	PASS


All Week25 engineering components work correctly and meet Bootcamp requirements:
- Validates analytics input
- Rejects malformed events
- Computes funnel conversion
- Computes A/B conversion
- Documents user flow instrumentation
Provides evidence-based testing

This project is ready for submission.