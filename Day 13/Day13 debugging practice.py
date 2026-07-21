"""
Day 13 - Debugging Practice
============================
This file demonstrates different types of bugs (Syntax, Runtime, Logical)
and various debugging techniques used to find and fix them.

Note: Some buggy code blocks are commented out on purpose so the whole
file can run without crashing. Uncomment them one at a time to see the
actual errors in action.
"""

# ======================================================
# 1. SYNTAX ERROR EXAMPLE (commented out - would crash)
# ======================================================
# Buggy version:
# def greet()
#     print("Hello")
#
# Fixed version:
def greet():
    print("Hello")


# ======================================================
# 2. RUNTIME ERROR EXAMPLES
# ======================================================

def divide_numbers(a, b):
    """Demonstrates ZeroDivisionError and how to handle it."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("DEBUG: Cannot divide by zero!")
        return None


def access_list_item(my_list, index):
    """Demonstrates IndexError and how to handle it."""
    try:
        return my_list[index]
    except IndexError:
        print(f"DEBUG: Index {index} is out of range for this list.")
        return None


def access_dict_key(my_dict, key):
    """Demonstrates KeyError and how to handle it."""
    try:
        return my_dict[key]
    except KeyError:
        print(f"DEBUG: Key '{key}' does not exist in the dictionary.")
        return None


def convert_to_int(value):
    """Demonstrates ValueError and how to handle it."""
    try:
        return int(value)
    except ValueError:
        print(f"DEBUG: Cannot convert '{value}' to an integer.")
        return None


# ======================================================
# 3. LOGICAL ERROR EXAMPLE
# ======================================================

def calculate_average_buggy(numbers):
    """BUGGY VERSION: has a logical error (extra -1)."""
    total = sum(numbers)
    average = total / len(numbers) - 1   # BUG: should not subtract 1
    return average


def calculate_average_fixed(numbers):
    """FIXED VERSION: correct formula."""
    total = sum(numbers)
    average = total / len(numbers)
    return average


# ======================================================
# 4. PRINT STATEMENT DEBUGGING
# ======================================================

def calculate_total_with_debug_prints(price, quantity):
    """Shows how print statements help trace variable values."""
    print(f"DEBUG: price = {price} ({type(price)})")
    print(f"DEBUG: quantity = {quantity} ({type(quantity)})")

    # Convert quantity to int if it's a string (common bug source)
    if isinstance(quantity, str):
        quantity = int(quantity)
        print(f"DEBUG: quantity converted to int -> {quantity}")

    total = price * quantity
    print(f"DEBUG: total = {total}")
    return total


# ======================================================
# 5. DIVIDE AND CONQUER DEBUGGING (breaking into steps)
# ======================================================

def fetch_data():
    """Simulates fetching raw data."""
    return [10, 20, 30, 40]


def process_data(data):
    """Simulates processing the data (e.g. doubling each value)."""
    return [item * 2 for item in data]


def analyze_data(data):
    """Simulates analyzing the data (e.g. calculating average)."""
    return sum(data) / len(data)


def run_pipeline_with_checks():
    """Runs each step separately and prints output to isolate bugs."""
    data = fetch_data()
    print("DEBUG Step 1 - fetch_data():", data)

    processed = process_data(data)
    print("DEBUG Step 2 - process_data():", processed)

    result = analyze_data(processed)
    print("DEBUG Step 3 - analyze_data():", result)

    return result


# ======================================================
# 6. TESTING WITH KNOWN INPUTS
# ======================================================

def test_calculate_average():
    """Uses a known input/output pair to verify correctness."""
    test_numbers = [10, 20, 30]
    expected = 20.0
    actual = calculate_average_fixed(test_numbers)

    if actual == expected:
        print(f"PASS: calculate_average_fixed({test_numbers}) = {actual}")
    else:
        print(f"FAIL: expected {expected}, got {actual}")


# ======================================================
# 7. FULL DEBUGGING EXAMPLE - Discount Calculator
# ======================================================

def calculate_discount(price, discount_percent):
    """Calculates the final price after applying a discount."""
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price


def run_discount_example():
    """
    BUG (originally): discount_percent was passed as a string "10"
    instead of an integer 10, causing a TypeError.
    FIX: pass discount_percent as an int.
    """
    items = [
        {"name": "Shirt", "price": 1000},
        {"name": "Shoes", "price": 3000},
    ]

    for item in items:
        discounted = calculate_discount(item["price"], 10)  # fixed: int, not "10"
        print(f"{item['name']}: Rs. {discounted}")


# ======================================================
# 8. COMMON BEGINNER BUG CHECKLIST (as functions to test)
# ======================================================

def check_assignment_vs_comparison():
    """Demonstrates the difference between = and ==."""
    x = 5          # assignment
    is_five = (x == 5)   # comparison
    print(f"x = {x}, is_five (x == 5) = {is_five}")


def check_infinite_loop_fix():
    """Shows a loop that could be infinite if not updated properly."""
    count = 0
    max_iterations = 5

    while count < max_iterations:   # BUG risk: forgetting to increment count
        print(f"DEBUG: loop iteration {count}")
        count += 1   # this line prevents an infinite loop


# ======================================================
# MAIN - Run all demonstrations
# ======================================================

if __name__ == "__main__":
    print("\n--- 1. Basic Function Test ---")
    greet()

    print("\n--- 2. Runtime Error Handling ---")
    print("Divide 10 by 0:", divide_numbers(10, 0))
    print("Divide 10 by 2:", divide_numbers(10, 2))

    fruits = ["apple", "banana"]
    print("Access index 5:", access_list_item(fruits, 5))
    print("Access index 1:", access_list_item(fruits, 1))

    student = {"name": "Ali", "age": 22}
    print("Access missing key 'grade':", access_dict_key(student, "grade"))
    print("Access existing key 'name':", access_dict_key(student, "name"))

    print("Convert 'abc' to int:", convert_to_int("abc"))
    print("Convert '42' to int:", convert_to_int("42"))

    print("\n--- 3. Logical Error Comparison ---")
    numbers = [10, 20, 30]
    print("Buggy average:", calculate_average_buggy(numbers))
    print("Fixed average:", calculate_average_fixed(numbers))

    print("\n--- 4. Print Statement Debugging ---")
    calculate_total_with_debug_prints(50, "3")

    print("\n--- 5. Divide and Conquer Debugging ---")
    run_pipeline_with_checks()

    print("\n--- 6. Testing with Known Inputs ---")
    test_calculate_average()

    print("\n--- 7. Full Debugging Example: Discount Calculator ---")
    run_discount_example()

    print("\n--- 8. Common Beginner Bug Checks ---")
    check_assignment_vs_comparison()
    check_infinite_loop_fix()

    print("\nAll debugging demonstrations completed successfully!")