def print_user_flow() -> None:
    steps = [
        "1. app_open (event: app_open)",
        "2. student_taps_ask_help_button (event: help_button_clicked)",
        "3. question_input_shown (event: question_input_shown)",
        "4. question_submitted (event: question_submitted)",
        "5. backend_calls_model (no user event, internal log)",
        "6. answer_received (event: answer_received)",
        "7. student_marks_helpful (event: helpful_marked)",
        "8. student_continues_learning (event: continue_learning_clicked)",
    ]

    print("Mobile-first user flow for AI Learning Help:")
    for s in steps:
        print(" -", s)

    print("\nInstrumentation points (events):")
    events = [
        "app_open",
        "help_button_clicked",
        "question_input_shown",
        "question_submitted",
        "answer_received",
        "helpful_marked",
        "continue_learning_clicked",
        "session_end",
    ]
    for e in events:
        print(" -", e)

    print("\nEach event should be tied to a question, for example:")
    print(" - app_open → How many users start the flow?")
    print(" - question_submitted → How many users actually ask for help?")
    print(" - answer_received → Is the system responding reliably?")
    print(" - helpful_marked → Do users find the help useful?")
    print(" - continue_learning_clicked → Does the help lead to continued learning?")

if __name__ == "__main__":
    print_user_flow()
