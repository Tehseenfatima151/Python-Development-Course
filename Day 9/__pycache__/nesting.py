#  Nesting (Dictionary ke andar Dictionary/List)
travel_log = {
    "France": {"visit_count": 12, "cities_visited": ["Paris", "Lille", "Dijon"]},
    "Germany": {"visit_count": 5, "cities_visited": ["Berlin", "Hamburg", "Stuttgart"]},
}

print(travel_log["France"]["cities_visited"])
# Output: ['Paris', 'Lille', 'Dijon']

print(travel_log["Germany"]["visit_count"])
# Output: 5

students = [
    {"name": "Ali", "age": 22},
    {"name": "Sara", "age": 21},
    {"name": "Ahmed", "age": 23}
]

for student in students:
    print(f"{student['name']} is {student['age']} years old")

# Output:
# Ali is 22 years old
# Sara is 21 years old
# Ahmed is 23 years olds