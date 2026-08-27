"""
Funnel Analyzer with proper sequence validation.
Week25 Engineering Assignment - AI Learning Platform

This analyzer ensures events are processed in chronological order
and validates that funnel steps occur in the correct sequence.
"""

import json
from typing import List, Dict, Tuple
from collections import defaultdict


# Core funnel definition for Week25
FUNNEL_STEPS = [
    "app_open",
    "question_submitted",
    "answer_received",
    "helpful_marked",
]


def load_events(logfile: str = "events.log") -> List[Dict]:
    """Load events from log file."""
    events = []
    try:
        with open(logfile, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                events.append(json.loads(line))
    except FileNotFoundError:
        print(f"No {logfile} found. Run event_logger.py first.")
    return events


def build_session_funnel(events: List[Dict]) -> Dict[str, Dict[str, any]]:
    """
    Build funnel data per session with proper sequence validation.
    
    Events are sorted by timestamp first, then we check if funnel steps
    occur in the correct order.
    
    Returns a dict where each session has:
    - step_reached: which steps were reached (in order)
    - max_step: the furthest step reached (index)
    - completed: whether the full funnel was completed
    """
    # Group events by session
    sessions_events = defaultdict(list)
    for e in events:
        sess = e.get("session_id")
        if sess:
            sessions_events[sess].append(e)
    
    sessions = {}
    for sess_id, sess_events in sessions_events.items():
        # Sort events by timestamp
        sess_events.sort(key=lambda e: e.get("timestamp", 0))
        
        # Track funnel progress
        session_data = {
            "step_reached": {step: False for step in FUNNEL_STEPS},
            "max_step": -1,
            "completed": False,
            "events_in_order": [],
        }
        
        current_step_idx = 0
        
        for event in sess_events:
            event_name = event.get("event_name", "")
            
            # Check if this event matches the current expected funnel step
            if current_step_idx < len(FUNNEL_STEPS):
                expected_step = FUNNEL_STEPS[current_step_idx]
                
                if event_name == expected_step:
                    # This is the next step in the funnel
                    session_data["step_reached"][event_name] = True
                    session_data["events_in_order"].append(event_name)
                    session_data["max_step"] = current_step_idx
                    current_step_idx += 1
                    
                    # Check if funnel is complete
                    if current_step_idx == len(FUNNEL_STEPS):
                        session_data["completed"] = True
        
        sessions[sess_id] = session_data
    
    return sessions


def analyze_funnel(sessions: Dict[str, Dict]) -> None:
    """Analyze and print funnel metrics."""
    total_sessions = len(sessions)
    if total_sessions == 0:
        print("No sessions to analyze.")
        return
    
    print("=" * 60)
    print("Funnel Analysis Report")
    print("=" * 60)
    print(f"\nTotal sessions: {total_sessions}")
    
    # Count sessions reaching each step
    step_counts = []
    for step in FUNNEL_STEPS:
        count = sum(1 for s in sessions.values() if s["step_reached"][step])
        step_counts.append(count)
    
    # Print funnel metrics
    prev_count = total_sessions
    print("\n--- Step-by-Step Conversion ---")
    for i, step in enumerate(FUNNEL_STEPS):
        count = step_counts[i]
        conversion_from_start = count / total_sessions if total_sessions > 0 else 0
        conversion_from_prev = count / prev_count if prev_count > 0 else 0
        dropoff = 1 - conversion_from_prev
        
        print(f"\nStep: {step}")
        print(f"  Users reaching step: {count}/{total_sessions}")
        print(f"  Conversion from start: {conversion_from_start:.2%}")
        print(f"  Conversion from previous: {conversion_from_prev:.2f}")
        print(f"  Drop-off from previous: {dropoff:.2%}")
        
        prev_count = count
    
    # Summary
    completed_count = sum(1 for s in sessions.values() if s["completed"])
    print("\n--- Summary ---")
    print(f"Full funnel completions: {completed_count}/{total_sessions}")
    print(f"Overall completion rate: {completed_count/total_sessions:.2%}" if total_sessions > 0 else "N/A")
    
    # Detect drop-off points
    if len(step_counts) >= 2:
        max_dropoff = 0
        max_dropoff_step = ""
        for i in range(1, len(step_counts)):
            dropoff = step_counts[i-1] - step_counts[i]
            if dropoff > max_dropoff:
                max_dropoff = dropoff
                max_dropoff_step = FUNNEL_STEPS[i]
        
        if max_dropoff > 0:
            print(f"\nLargest drop-off: {max_dropoff} users at '{max_dropoff_step}'")


def test_funnel_sequence() -> None:
    """Test that funnel correctly handles out-of-order events."""
    print("\n" + "=" * 60)
    print("Testing Funnel Sequence Validation")
    print("=" * 60)
    
    # Simulate events where helpful_marked comes before answer_received
    test_events = [
        {"event_name": "app_open", "timestamp": 1.0, "session_id": "test_1"},
        {"event_name": "question_submitted", "timestamp": 2.0, "session_id": "test_1"},
        {"event_name": "helpful_marked", "timestamp": 3.0, "session_id": "test_1"},  # Out of order!
        {"event_name": "answer_received", "timestamp": 4.0, "session_id": "test_1"},
    ]
    
    sessions = build_session_funnel(test_events)
    
    print("\nTest case: helpful_marked before answer_received")
    print(f"Session 'test_1' reached steps: {sessions['test_1']['events_in_order']}")
    print(f"Max step reached: {sessions['test_1']['max_step']} ({FUNNEL_STEPS[sessions['test_1']['max_step']] if sessions['test_1']['max_step'] >= 0 else 'none'})")
    print(f"Funnel completed: {sessions['test_1']['completed']}")
    
    # After sorting by timestamp and processing in order:
    # app_open (step 0) -> question_submitted (step 1) -> helpful_marked (not step 2, skipped) -> answer_received (step 2)
    # The funnel reaches answer_received but NOT helpful_marked because it was seen out of order
    # So funnel is NOT complete (needs all 4 steps in order)
    assert sessions['test_1']['step_reached']['app_open'] == True
    assert sessions['test_1']['step_reached']['question_submitted'] == True
    assert sessions['test_1']['step_reached']['answer_received'] == True  # This IS reached (comes after helpful_marked in time)
    assert sessions['test_1']['completed'] == False  # But funnel not complete because helpful_marked was out of order
    
    print("\n✓ Test PASSED: Out-of-order events correctly handled")


if __name__ == "__main__":
    # Run tests first
    test_funnel_sequence()
    
    # Then analyze actual events
    print("\n\n")
    events = load_events()
    if events:
        sessions = build_session_funnel(events)
        analyze_funnel(sessions)
    else:
        print("No events to analyze. Run event_logger.py first.")
