from typing import List, Dict

def calculate_conversion(exposed: int, completed: int) -> float:
    if exposed == 0:
        return 0.0
    return completed / exposed

def analyze_ab(data: List[Dict]) -> None:
    for variant in data:
        name = variant["name"]
        exposed = variant["exposed"]
        completed = variant["completed"]
        conv = calculate_conversion(exposed, completed)
        print(f"Variant {name}: exposed={exposed}, completed={completed}, conversion={conv:.2f}")

    diff = calculate_conversion(data[1]["exposed"], data[1]["completed"]) - \
           calculate_conversion(data[0]["exposed"], data[0]["completed"])
    print(f"Difference B - A: {diff:.2f}")
    print("Note: With small sample sizes, this difference is exploratory, not statistically conclusive.")

def main() -> None:
    # Example dataset from assignment: A = 40/18, B = 42/25
    ab_data = [
        {"name": "A", "exposed": 40, "completed": 18},
        {"name": "B", "exposed": 42, "completed": 25},
    ]
    analyze_ab(ab_data)

if __name__ == "__main__":
    main()
