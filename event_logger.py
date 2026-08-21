import json
import time
from typing import Dict, Any, List

ALLOWED_EVENTS = {
    "app_open",
    "question_submitted",
    "answer_received",
    "helpful_marked",
    "plan_created",
    "plan_completed",
    "feedback_submitted",
    "session_end",
}

def validate_event(event: Dict[str, Any]) -> bool:
    if "event_name" not in event:
        return False
    if event["event_name"] not in ALLOWED_EVENTS:
        return False

    if "timestamp" not in event:
        return False
    if not isinstance(event["timestamp"], (int, float)):
        return False

    if "session_id" not in event or not isinstance(event["session_id"], str):
        return False

    if "variant" in event and not isinstance(event["variant"], str):
        return False

    if "properties" in event and not isinstance(event["properties"], dict):
        return False

    return True

def log_event(event: Dict[str, Any], logfile: str = "events.log") -> None:
    if not validate_event(event):
        print("Rejected invalid event:", event)
        return

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    print("Logged event:", event["event_name"])

def demo_events() -> None:
    now = time.time()
    events = [
        {
            "event_name": "app_open",
            "timestamp": now,
            "session_id": "sess_1",
            "variant": "A",
            "properties": {"device": "mobile"},
        },
        {
            "event_name": "question_submitted",
            "timestamp": now + 5,
            "session_id": "sess_1",
            "variant": "A",
            "properties": {"subject": "math"},
        },
        {
            "event_name": "answer_received",
            "timestamp": now + 7,
            "session_id": "sess_1",
            "variant": "A",
            "properties": {"latency_ms": 2000},
        },
        {
            "event_name": "helpful_marked",
            "timestamp": now + 15,
            "session_id": "sess_1",
            "variant": "A",
            "properties": {"rating": 5},
        },
        # invalid event (should be rejected)
        {
            "event_name": "unknown_event",
            "timestamp": now,
            "session_id": "sess_2",
            "properties": {},
        },
    ]

    for e in events:
        log_event(e)

if __name__ == "__main__":
    demo_events()
