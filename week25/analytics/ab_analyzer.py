"""
A/B Test Analyzer with input validation.
Week25 Engineering Assignment - AI Learning Platform

This analyzer validates input data and handles edge cases properly.
"""

from typing import List, Dict


def validate_ab_input(data: List[Dict]) -> tuple[bool, str]:
    """
    Validate A/B test input data.
    
    Checks:
    - At least 2 variants (A and B)
    - exposed >= 0
    - completed >= 0
    - completed <= exposed
    - All required fields present
    
    Returns (is_valid, error_message).
    """
    if len(data) < 2:
        return False, "A/B test requires at least 2 variants"
    
    for variant in data:
        # Check required fields
        if "name" not in variant:
            return False, "Missing 'name' field"
        if "exposed" not in variant:
            return False, f"Missing 'exposed' field for variant {variant.get('name', '?')}"
        if "completed" not in variant:
            return False, f"Missing 'completed' field for variant {variant.get('name', '?')}"
        
        exposed = variant["exposed"]
        completed = variant["completed"]
        
        # Validate types
        if not isinstance(exposed, (int, float)):
            return False, f"'exposed' must be a number for variant {variant['name']}"
        if not isinstance(completed, (int, float)):
            return False, f"'completed' must be a number for variant {variant['name']}"
        
        # Validate ranges
        if exposed < 0:
            return False, f"'exposed' cannot be negative for variant {variant['name']}: {exposed}"
        if completed < 0:
            return False, f"'completed' cannot be negative for variant {variant['name']}: {completed}"
        if completed > exposed:
            return False, f"'completed' ({completed}) > 'exposed' ({exposed}) for variant {variant['name']}"
    
    return True, ""


def calculate_conversion(exposed: int, completed: int) -> float:
    """
    Calculate conversion rate with validation.
    
    Args:
        exposed: Number of users exposed to the variant
        completed: Number of users who completed the action
    
    Returns:
        Conversion rate as a float (0.0 to 1.0)
    
    Raises:
        ValueError: If inputs are invalid
    """
    if exposed < 0:
        raise ValueError(f"exposed cannot be negative: {exposed}")
    if completed < 0:
        raise ValueError(f"completed cannot be negative: {completed}")
    if completed > exposed:
        raise ValueError(f"completed ({completed}) cannot exceed exposed ({exposed})")
    
    if exposed == 0:
        return 0.0
    return completed / exposed


def analyze_ab(data: List[Dict]) -> Dict:
    """
    Analyze A/B test data and return results.
    
    Args:
        data: List of variant dictionaries with name, exposed, completed
    
    Returns:
        Dictionary with analysis results
    """
    # Validate input first
    is_valid, error_msg = validate_ab_input(data)
    if not is_valid:
        raise ValueError(error_msg)
    
    results = []
    for variant in data:
        name = variant["name"]
        exposed = variant["exposed"]
        completed = variant["completed"]
        conv = calculate_conversion(exposed, completed)
        
        results.append({
            "name": name,
            "exposed": exposed,
            "completed": completed,
            "conversion": conv,
        })
    
    # Calculate difference between B and A
    if len(results) >= 2:
        diff = results[1]["conversion"] - results[0]["conversion"]
    else:
        diff = 0.0
    
    # Calculate statistical notes
    total_exposed = sum(v["exposed"] for v in results)
    small_sample = total_exposed < 100
    
    return {
        "variants": results,
        "difference": diff,
        "small_sample_warning": small_sample,
        "total_exposed": total_exposed,
    }


def print_analysis(results: Dict) -> None:
    """Print A/B analysis results in a readable format."""
    print("=" * 60)
    print("A/B Test Analysis Report")
    print("=" * 60)
    
    print("\n--- Variant Results ---")
    for variant in results["variants"]:
        print(f"\nVariant {variant['name']}:")
        print(f"  Exposed: {variant['exposed']}")
        print(f"  Completed: {variant['completed']}")
        print(f"  Conversion Rate: {variant['conversion']:.2%}")
    
    print("\n--- Comparison ---")
    if len(results["variants"]) >= 2:
        print(f"Difference (B - A): {results['difference']:+.2%}")
        
        if results["difference"] > 0:
            print(f"Variant B performs {results['difference']:.2%} better than Variant A")
        elif results["difference"] < 0:
            print(f"Variant A performs {-results['difference']:.2%} better than Variant B")
        else:
            print("Both variants have equal conversion rates")
    
    print("\n--- Statistical Notes ---")
    print(f"Total exposed users: {results['total_exposed']}")
    if results["small_sample_warning"]:
        print("⚠️  WARNING: Small sample size (< 100 users)")
        print("   Results are EXPLORATORY only - cannot claim causality")
        print("   Need more data for statistical significance")
    else:
        print("✓ Sample size adequate for preliminary analysis")


def demo_ab_test() -> None:
    """Demonstrate A/B analyzer with various test cases."""
    print("=" * 60)
    print("A/B Analyzer Demo")
    print("=" * 60)
    
    # Test 1: Valid dataset from assignment
    print("\n--- Test 1: Valid A/B Dataset ---")
    valid_data = [
        {"name": "A", "exposed": 40, "completed": 18},
        {"name": "B", "exposed": 42, "completed": 25},
    ]
    
    try:
        results = analyze_ab(valid_data)
        print_analysis(results)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test 2: Invalid - completed > exposed
    print("\n\n--- Test 2: Invalid Data (completed > exposed) ---")
    invalid_data = [
        {"name": "A", "exposed": 40, "completed": 45},  # Invalid!
        {"name": "B", "exposed": 42, "completed": 25},
    ]
    
    try:
        results = analyze_ab(invalid_data)
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Test 3: Invalid - negative values
    print("\n\n--- Test 3: Invalid Data (negative values) ---")
    invalid_data2 = [
        {"name": "A", "exposed": -10, "completed": 5},  # Invalid!
        {"name": "B", "exposed": 42, "completed": 25},
    ]
    
    try:
        results = analyze_ab(invalid_data2)
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Test 4: Edge case - zero exposed
    print("\n\n--- Test 4: Edge Case (zero exposed) ---")
    edge_data = [
        {"name": "A", "exposed": 0, "completed": 0},
        {"name": "B", "exposed": 50, "completed": 30},
    ]
    
    try:
        results = analyze_ab(edge_data)
        print_analysis(results)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test 5: Only one variant
    print("\n\n--- Test 5: Invalid - Only One Variant ---")
    single_variant = [
        {"name": "A", "exposed": 40, "completed": 18},
    ]
    
    try:
        results = analyze_ab(single_variant)
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_ab_test()
