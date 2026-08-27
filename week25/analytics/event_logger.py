"""
Event Logger with validation, deduplication, and impossible sequence detection.
Week25 Engineering Assignment - AI Learning Platform
"""

import json
import time
from typing import Dict, Any, Optional, Set, Tuple

# Handle both direct execution and module import
try:
    from analytics.event_schema import ALLOWED_EVENTS, REQUIRED_FIELDS, FIELD_TYPES, is_event_allowed
except ImportError:
    from event_schema import ALLOWED_EVENTS, REQUIRED_FIELDS, FIELD_TYPES, is_event_allowed


class EventLogger:
    """
    Event logger with:
    - Schema validation
    - Duplicate detection (session_id + event_name + timestamp)
    - Impossible sequence detection
    """

    def __init__(self, logfile: str = "events.log"):
        self.logfile = logfile
        self._seen_events: Set[Tuple[str, str, float]] = set()  # For deduplication
        self._session_events: Dict[str, list] = {}  # For sequence validation

    def _validate_event(self, event: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate event against schema. Returns (is_valid, error_message)."""
        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in event:
                return False, f"Missing required field: {field}"

        # Check event_name is allowed
        if not is_event_allowed(event["event_name"]):
            return False, f"Invalid event_name: {event['event_name']}"

        # Check types
        for field, expected_type in FIELD_TYPES.items():
            if field in event:
                value = event[field]
                if isinstance(expected_type, tuple):
                    if not isinstance(value, expected_type):
                        return False, f"Field '{field}' must be one of types {expected_type}"
                else:
                    if not isinstance(value, expected_type):
                        return False, f"Field '{field}' must be of type {expected_type.__name__}"

        return True, ""

    def _is_duplicate(self, event: Dict[str, Any]) -> bool:
        """Check if this event is a duplicate."""
        session_id = event.get("session_id", "")
        event_name = event.get("event_name", "")
        timestamp = event.get("timestamp", 0.0)
        
        event_key = (session_id, event_name, timestamp)
        if event_key in self._seen_events:
            return True
        
        self._seen_events.add(event_key)
        return False

    def _check_impossible_sequence(self, event: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check for impossible sequences.
        Returns (is_valid, error_message).
        
        Rules:
        - plan_completed requires plan_created first
        - answer_received requires question_submitted first
        - helpful_marked requires answer_received first
        """
        session_id = event.get("session_id", "")
        event_name = event.get("event_name", "")
        
        if session_id not in self._session_events:
            self._session_events[session_id] = []
        
        # Check specific sequence rules
        if event_name == "plan_completed":
            if "plan_created" not in self._session_events[session_id]:
                return False, "Impossible sequence: plan_completed without prior plan_created"
        
        elif event_name == "answer_received":
            if "question_submitted" not in self._session_events[session_id]:
                return False, "Impossible sequence: answer_received without prior question_submitted"
        
        elif event_name == "helpful_marked":
            if "answer_received" not in self._session_events[session_id]:
                return False, "Impossible sequence: helpful_marked without prior answer_received"
        
        # Record this event
        self._session_events[session_id].append(event_name)
        return True, ""

    def log_event(self, event: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Log an event after validation.
        Returns (success, message).
        """
        # Validate schema
        is_valid, error_msg = self._validate_event(event)
        if not is_valid:
            return False, f"Schema validation failed: {error_msg}"

        # Check for duplicates
        if self._is_duplicate(event):
            return False, "Rejected duplicate event"

        # Check for impossible sequences
        is_valid, error_msg = self._check_impossible_sequence(event)
        if not is_valid:
            return False, error_msg

        # Write to log file
        try:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
            return True, f"Logged event: {event['event_name']}"
        except Exception as e:
            return False, f"Failed to write event: {str(e)}"


def demo_events() -> None:
    """Demonstrate the event logger with various test cases."""
    logger = EventLogger()
    now = time.time()
    
    print("=" * 60)
    print("Event Logger Demo")
    print("=" * 60)
    
    # Test 1: Valid events in correct sequence
    print("\n--- Test 1: Valid event sequence ---")
    valid_events = [
        {
            "event_name": "app_open",
            "timestamp": now,
            "session_id": "sess_1",
            "variant": "A",
            "properties": {"device": "mobile"},
        },
        {
            "event_name": "help_button_clicked",
            "timestamp": now + 2,
            "session_id": "sess_1",
            "variant": "A",
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
        {
            "event_name": "continue_learning_clicked",
            "timestamp": now + 20,
            "session_id": "sess_1",
            "variant": "A",
        },
    ]
    
    for event in valid_events:
        success, msg = logger.log_event(event)
        print(f"{msg}")
    
    # Test 2: Invalid event name
    print("\n--- Test 2: Invalid event name ---")
    invalid_event = {
        "event_name": "unknown_event",
        "timestamp": now,
        "session_id": "sess_2",
    }
    success, msg = logger.log_event(invalid_event)
    print(f"{msg}")
    
    # Test 3: Duplicate event
    print("\n--- Test 3: Duplicate event (should be rejected) ---")
    duplicate_event = {
        "event_name": "app_open",
        "timestamp": now,
        "session_id": "sess_1",
        "variant": "A",
    }
    success, msg = logger.log_event(duplicate_event)
    print(f"{msg}")
    
    # Test 4: Impossible sequence (helpful_marked without answer_received)
    print("\n--- Test 4: Impossible sequence (new session) ---")
    logger2 = EventLogger()
    impossible_event = {
        "event_name": "helpful_marked",
        "timestamp": now + 100,
        "session_id": "sess_new",
    }
    success, msg = logger2.log_event(impossible_event)
    print(f"{msg}")
    
    # Test 5: Missing required field
    print("\n--- Test 5: Missing required field ---")
    missing_field_event = {
        "event_name": "app_open",
        "timestamp": now,
        # Missing session_id
    }
    success, msg = logger.log_event(missing_field_event)
    print(f"{msg}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_events()
