"""
Centralized Event Schema for Week25 AI Learning Platform.
All modules must import from this file to ensure consistency.
"""

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

REQUIRED_FIELDS = {"event_name", "timestamp", "session_id"}

OPTIONAL_FIELDS = {"variant", "properties"}

FIELD_TYPES = {
    "event_name": str,
    "timestamp": (int, float),
    "session_id": str,
    "variant": str,
    "properties": dict,
}


def get_allowed_events() -> set:
    """Return the set of allowed event names."""
    return ALLOWED_EVENTS.copy()


def is_event_allowed(event_name: str) -> bool:
    """Check if an event name is in the allowed list."""
    return event_name in ALLOWED_EVENTS


def get_required_fields() -> set:
    """Return the set of required fields."""
    return REQUIRED_FIELDS.copy()


def validate_event_schema(event: dict) -> tuple[bool, str]:
    """
    Validate an event against the schema.
    Returns (is_valid, error_message).
    """
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
