# Week25 Academic Product — AI Learning Platform V2

## User Validation Release

**Student:** Mingtao  
**Date:** 2026-08-22  
**Bootcamp V2.0 — Week 25**

---

## 1. Target User + Core Problem

### Target User
High school students (ages 14-18) who need quick, personalized help with homework questions but may not have immediate access to teachers or tutors.

### Core Problem
Students often get stuck on homework problems outside of class hours. They need:
- Instant answers to specific questions
- Explanations that help them understand, not just copy
- A simple, mobile-friendly interface they can use anywhere

---

## 2. Core User Flow (End-to-End)

```
Open App
    ↓
Tap "Ask a Question"
    ↓
Type Question
    ↓
Submit → Receive AI Answer
    ↓
Mark "Helpful" or "Not Helpful"
    ↓
Continue Learning (ask another question)
```

**Instrumented Events:**
- `app_open` — User opens the app
- `help_button_clicked` — User taps "Ask Question"
- `question_input_shown` — Question input form displayed
- `question_submitted` — User submits their question
- `answer_received` — AI response displayed
- `helpful_marked` or `feedback_submitted` — User provides feedback
- `continue_learning_clicked` — User continues to next question

---

## 3. User Stories (with Acceptance Criteria)

### Story 1: Student — Quick Homework Help

**As a** high school student  
**I want to** quickly ask a question and get an answer  
**So that** I can continue my homework without getting stuck

**Acceptance Criteria:**
- [ ] Can open app on mobile phone
- [ ] Can type or paste a question in under 30 seconds
- [ ] Receives an answer within 5 seconds
- [ ] Can mark if the answer was helpful
- [ ] Can immediately ask another question

---

### Story 2: Teacher — Understanding Student Struggles

**As a** teacher  
**I want to** see what types of questions students are asking  
**So that** I can identify common areas of confusion and adjust my lessons

**Acceptance Criteria:**
- [ ] Analytics dashboard shows question topics
- [ ] Can see which answers were marked "not helpful"
- [ ] Can identify patterns in student struggles
- [ ] Data is anonymous (no student names)

---

### Story 3: Parent — Monitoring Learning Progress

**As a** parent  
**I want to** know my child is getting quality help  
**So that** I feel confident they're learning effectively

**Acceptance Criteria:**
- [ ] Can see how many questions child has asked
- [ ] Can see feedback ratings (helpful vs not helpful)
- [ ] Privacy protected — no personal data exposed
- [ ] Simple summary view (not overwhelming)

---

## 4. Event Instrumentation

All events follow a centralized schema defined in `analytics/event_schema.py`:

| Event Name | Trigger Point | Properties |
|------------|---------------|------------|
| `app_open` | App loads | device type |
| `help_button_clicked` | Taps "Ask Question" | - |
| `question_input_shown` | Form rendered | - |
| `question_submitted` | Form submitted | question_length, subject |
| `answer_received` | Answer displayed | answer_length, latency |
| `helpful_marked` | Clicks 👍 | rating (1-5) |
| `feedback_submitted` | Clicks 👎 | feedback_type |
| `continue_learning_clicked` | Asks another question | - |
| `session_end` | Closes app or 5min idle | session_duration |

**Schema Validation:**
- All events must include: `event_name`, `timestamp`, `session_id`
- Event names are validated against whitelist
- Duplicate events (same session+event+timestamp) are rejected
- Impossible sequences detected (e.g., `helpful_marked` before `answer_received`)

---

## 5. Feedback Mechanism

### In-App Feedback Buttons

After receiving an answer, users see:
- 👍 **"Yes, Helpful!"** — Logs `helpful_marked` event
- 👎 **"Not Helpful"** — Logs `feedback_submitted` event

### Optional Follow-up
For "Not Helpful" feedback, users can optionally select:
- "Answer was unclear"
- "Answer was incorrect"
- "Too complicated"
- "Other"

This minimal feedback approach:
- Takes < 3 seconds
- Doesn't require typing
- Provides actionable data

---

## 6. A/B Testing Plan

### Hypothesis
Simpler question input (single field) will have higher completion rate than multi-field form.

### Test Design

| Variant | Description | Metric |
|---------|-------------|--------|
| A (Control) | Single text area: "Type your question" | Question submission rate |
| B (Test) | Two fields: "Subject" + "Your question" | Question submission rate |

### Success Criteria
- Primary: Question submission rate increases by ≥15%
- Secondary: Time-to-submit decreases
- Guardrail: No decrease in "helpful" ratings

### Analysis Method
- Use `ab_analyzer.py` to compare conversion rates
- Minimum 100 users per variant for statistical validity
- Run test for 7 days minimum

---

## 7. User Testing Report

### Test Session: August 22, 2026

**Task:** Ask a math question and evaluate the answer

| Tester | Role | Completed? | Time | Confusion Points | Comments |
|--------|------|------------|------|------------------|----------|
| Tester 1 | Student (Grade 10) | ✅ Yes | 45 sec | None | "Very easy to use. Answer was clear." |
| Tester 2 | Parent | ✅ Yes | 60 sec | Where to find history | "Good for helping my kid. Would like to see past questions." |

### Top 3 Improvements (Based on Testing)

1. **Add question history** — Both testers wanted to see previous questions
2. **Add subject tags** — Parent suggested categorizing by subject
3. **Add share feature** — Student wanted to share answers with classmates

---

## 8. Security & Privacy Notes

### Data Minimization
- Only anonymous session IDs stored (no names, emails, or personal info)
- Question text logged only for analytics (not stored permanently)
- No third-party tracking

### Input Validation
- All events validated against schema before logging
- Duplicate events rejected
- Impossible sequences detected and flagged

### Future Considerations (Not Implemented)
- Rate limiting (prevent spam)
- Authentication for returning users
- Server-side validation of critical events
- GDPR compliance for EU users

---

## 9. Mobile-First Usability

### Design Decisions

| Feature | Mobile Optimization |
|---------|---------------------|
| Layout | Single column, full-width buttons |
| Touch Targets | All buttons ≥48px height |
| Text Size | 16px minimum (no zoom required) |
| Loading States | Immediate feedback on all actions |
| Network Resilience | Graceful degradation on slow connections |

### Responsive Breakpoints
- Default: Mobile (< 480px)
- Tablet: 480–768px (tested)
- Desktop: > 768px (functional but not primary target)

---

## 10. Implementation Evidence

### Before/After Comparison

**Before (Week 24):**
- Static platform with no user feedback
- No analytics instrumentation
- No way to measure effectiveness

**After (Week 25 MVP):**
- ✅ Full core flow implemented and instrumented
- ✅ Feedback mechanism (👍/👎) integrated
- ✅ Event logging with validation
- ✅ Funnel analysis capability
- ✅ A/B testing framework ready
- ✅ User testing completed with 2 participants

### Key Metrics from MVP Testing

| Metric | Value |
|--------|-------|
| Sessions tested | 2 |
| Questions asked | 2 |
| Helpful ratings | 1/2 (50%) |
| Completion rate | 2/2 (100%) |

**Note:** Sample size is too small for statistical conclusions. This is exploratory data only.

---

## 11. Next Steps

### Immediate (Week 26)
1. Recruit 10+ real users for testing
2. Implement question history feature
3. Add subject tagging

### Short-term (Month 2)
1. Connect to real AI API
2. Build teacher dashboard
3. Implement A/B test with actual users

### Long-term (Month 3+)
1. Add authentication
2. Implement rate limiting
3. Expand to multiple subjects

---

## 12. Conclusion

This Week 25 MVP successfully transforms the Week 24 platform into a testable product with:
- Clear target user and problem statement
- End-to-end instrumented user flow
- Real feedback mechanism
- Proper event validation and security
- Mobile-first design
- Initial user validation

The foundation is now in place for iterative improvement based on real user data.
