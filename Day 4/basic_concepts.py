# Useful List Functions
import random


numbers = [5, 3, 8, 1, 9]

print(len(numbers))     # List ki length -> 5
print(max(numbers))     # Sabse bara number -> 9
print(min(numbers))     # Sabse chota number -> 1
print(sum(numbers))     # Sab ka sum -> 26

numbers.sort()           # Ascending order
print(numbers)           # [1, 3, 5, 8, 9]

numbers.reverse()        # List ko ulta karna
print(numbers)           # [9, 8, 5, 3, 1]

# random.choice() — List se random element choose karna
colors = ["red", "blue", "green", "yellow"]
picked = random.choice(colors)
print(picked)   # List mein se koi bhi ek random color

# random.shuffle() — List ko shuffle (mix) karna

cards = ["A", "K", "Q", "J", "10"]
random.shuffle(cards)
print(cards)   # Order har dafa alag hoga

# 6

numbers = [1, 2, 3, 9, 5]

print(random.sample(numbers, 2))

# 7
print(random.uniform(1, 10))

# 8 SMS
print("Welcome to the Student Management System!")
student_list = ["Tehseen", "Ali", "Adeel", "Asad", "Bilal", "Hamza", "Hammad", "Imran", "Junaid", "Kashif", "Muhammad", "Nadeem", "Omer", "Qasim", "Raza", "Salman", "Shahbaz", "Talha", "Usman"]
while True:
    print("\nMenu:")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Search Student")
    print("4. Show All Students")
    print("5. Exit")

    choice = int(input("Enter your choice (1-5): "))
    if choice == 1:
        name = input("Enter student name: ")
        student_list.append(name)
        print(f"Student {name} added successfully!")
    elif choice == 2:
        name = input("Enter student name to remove: ")
        if name in student_list:
            student_list.remove(name)
            print(f"Student {name} removed successfully!")
        else:
            print(f"Student {name} does not exist in the record.")
    elif choice == 3:
        name = input("Enter student name to search: ")
        if name in student_list:
            print(f"Student {name} exists in the record!")
        else:
            print(f"Student {name} does not exist in the record.")
    elif choice == 4:
        student_list= enumerate(student_list, start=1)
        print("List of all students is:")
        for i, name in student_list:
            print(f"{i}. {name}")
    elif choice == 5:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid Choice")
    
print("Thank you for using the Student Management System!")
