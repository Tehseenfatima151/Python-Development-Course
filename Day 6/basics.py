def greet(name):
    print(f"Hello, {name}!")

greet("Tehseen")     # Output: Tehseen, Ali!
greet("Sara")    # Output: Hello, Sara!

def add_numbers(a, b):
    print(f"Sum is: {a + b}")

add_numbers(5, 3)   # Output: Sum is: 8

def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()          # Output: Hello, Guest!
greet("Ahmed")   # Output: Hello, Ahmed!


def add_numbers(a, b):
    return a + b

result = add_numbers(4, 6)
print(result)    # Output: 10
print(result * 2)  # Output: 20  (return ki hui value use ho sakti hai)

