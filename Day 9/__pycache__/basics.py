# Creating & Accessing a Dictionary
student = {
    "name": "Ali",
    "age": 22,
    "course": "Software Engineering"
}

print(student["name"])    # Output: Ali
print(student["age"])     # Output: 22

# Adding, Updating & Removing Items

pythonstudent = {"name": "Ali", "age": 22}

# Naya key-value add karna
student["city"] = "Burewala"
print(student)   # {'name': 'Ali', 'age': 22, 'city': 'Burewala'}

# Existing value update karna
student["age"] = 23
print(student)   # {'name': 'Ali', 'age': 23, 'city': 'Burewala'}

# Item remove karna
del student["city"]
print(student)   # {'name': 'Ali', 'age': 23}

# Looping through a Dictionary

pythonstudent = {"name": "Ali", "age": 22, "course": "Software Engineering"}

for key in student:
    print(key, ":", student[key])

# Output:
# name : Ali
# age : 22
# course : Software Engineering