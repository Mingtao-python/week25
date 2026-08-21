import json
from typing import List, Dict

FUNNEL_STEPS = [
    "app_open",
    "question_submitted",
    "answer_received",
    "helpful_marked",
]

def load_events(logfile: str = "events.log") -> List[Dict]:
    events = []
    try:
        with open(logfile, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                events.append(json.loads(line))
    except FileNotFoundError:
        print("No events.log found. Run event_logger.py first.")
    return events

def build_session_funnel(events: List[Dict]) -> Dict[str, Dict[str, bool]]:
    sessions: Dict[str, Dict[str, bool]] = {}
    for e in events:
        sess = e.get("session_id")
        name = e.get("event_name")
        if not sess or not name:
            continue
        if sess not in sessions:
            sessions[sess] = {step: False for step in FUNNEL_STEPS}
        if name in sessions[sess]:
            sessions[sess][name] = True
    return sessions

def analyze_funnel(sessions: Dict[str, Dict[str, bool]]) -> None:
    total_sessions = len(sessions)
    if total_sessions == 0:
        print("No sessions to analyze.")
        return

    print(f"Total sessions: {total_sessions}")
    prev_count = total_sessions

    for step in FUNNEL_STEPS:
        count = sum(1 for s in sessions.values() if s[step])
        conversion = count / prev_count if prev_count > 0 else 0
        dropoff = 1 - conversion
        print(f"Step: {step}")
        print(f"  Users reaching step: {count}")
        print(f"  Conversion from previous: {conversion:.2f}")
        print(f"  Drop-off from previous: {dropoff:.2f}")
        prev_count = count

def main() -> None:
    events = load_events()
    sessions = build_session_funnel(events)
    analyze_funnel(sessions)

if __name__ == "__main__":
    main()
