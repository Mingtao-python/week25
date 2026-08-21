# Week25_Engineering  
AI Learning Platform — MVP, User Validation & Product Analytics  
Bootcamp V2.0 — Week 25 Engineering Deliverables

This repository contains the engineering components required for Week25:
- Event Logger  
- Funnel Analyzer  
- A/B Test Analyzer  
- User Flow Instrumentation  
- Testing Report  

These tools support the Week25 goal: **validate product hypotheses using real user behaviour, analytics events, funnels and controlled comparisons.**

---

# 1. Project Structure

```
Week25_Engineering/
│
├── event_logger.py
├── funnel_analyzer.py
├── ab_analyzer.py
├── user_flow_instrumentation.py
├── testing_report.md
└── events.log   (auto-generated)
```

---

# 2. Purpose of Each Module

### **event_logger.py**
A minimal analytics event logger with validation rules:
- Rejects invalid event names  
- Rejects missing fields  
- Rejects wrong types  
- Logs valid events to `events.log`  

### **funnel_analyzer.py**
Reads `events.log` and calculates:
- Step-by-step conversion  
- Drop-off rate  
- Funnel completion  

### **ab_analyzer.py**
Calculates conversion rates for A/B variants:
- Conversion = completed / exposed  
- Difference between A and B  
- Notes uncertainty for small samples  

### **user_flow_instrumentation.py**
Prints a mobile-first user flow and the events required to measure it.

### **testing_report.md**
Manual test report documenting:
- Expected vs actual behaviour  
- Pass/fail results  
- Invalid event tests  
- Funnel edge cases  
- A/B uncertainty notes  

---

# 3. How to Run

Open terminal in the project folder:

```bash
cd Week25_Engineering
```

### 3.1 Run Event Logger

```
python event_logger.py
```

Expected output:

```
Logged event: app_open
Logged event: question_submitted
Logged event: answer_received
Logged event: helpful_marked
Rejected invalid event: {...}
```

### 3.2 Run Funnel Analyzer

```
python funnel_analyzer.py
```

Expected output:

```
Total sessions: 1
Step: app_open → conversion 1.00
Step: question_submitted → conversion 1.00
Step: answer_received → conversion 1.00
Step: helpful_marked → conversion 1.00
```

### 3.3 Run A/B Analyzer

```
python ab_analyzer.py
```

Expected output:

```
Variant A: conversion=0.45
Variant B: conversion=0.60
Difference B - A: 0.15
Note: small sample → exploratory only
```

### 3.4 Run User Flow Instrumentation

```
python user_flow_instrumentation.py
```

---

# 4. Event Schema

Every event must follow this schema:

```json
{
  "event_name": "string (allowed)",
  "timestamp": "float (unix time)",
  "session_id": "string",
  "variant": "string (optional)",
  "properties": "object (optional)"
}
```
Allowed event names:

```
app_open
help_button_clicked
question_input_shown
question_submitted
answer_received
helpful_marked
continue_learning_clicked
plan_created
plan_completed
feedback_submitted
session_end
```

Invalid events are rejected automatically.

# 5. Funnel Definition
The core funnel for Week25:

```
app_open
→ question_submitted
→ answer_received
→ helpful_marked
```

Funnel Analyzer calculates:
- Users reaching each step
- Conversion from previous step
- Drop-off from previous step
- This supports Week25’s requirement: measure whether students actually reach useful AI help.

# 6. A/B Testing Definition
Example dataset:

A: 40 exposed / 18 completed

B: 42 exposed / 25 completed

Conversion:

A = 18/40 = 0.45

B = 25/42 = 0.60

Difference = 0.15

The analyzer also warns:

- Small samples → cannot claim causality
- Results are exploratory

This matches Week25’s requirement: avoid overclaiming causation.

# 7. Data Security & Validation
Week25 requires treating analytics as untrusted input.

This project includes:

- Event name whitelist
- Type validation
- Required fields
- Rejection of malformed events
- No personal data stored
- Only anonymous session IDs

This satisfies Week25’s Product Data Security module.

# 8. Testing Report
See testing_report.md for:

- Valid event tests
- Invalid event tests
- Funnel edge cases
- A/B uncertainty notes
- Expected vs actual results

This fulfills Week25’s requirement: evidence-based engineering.

# 9. Summary
This repository demonstrates the engineering skills required for Week25:

- MVP validation
- User flow instrumentation
- Analytics event logging
- Funnel analysis
- A/B comparison
- Evidence-based deciion making
- Data minimisation & validation

It is fully runnable, fully validated, and ready for submission.