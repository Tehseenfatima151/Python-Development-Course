# task 1
student_heights = input("Input a list of student heights ").split()
for n in range(0, len(student_heights)):
    student_heights[n] = int(student_heights[n])
total_height = 0
for height in student_heights:
    total_height += height
print(f"total height = {total_height}")

number_of_students = 0
for student in student_heights:
    number_of_students += 1
print(f"number of students = {number_of_students}")

average_height = round(total_height / number_of_students)
print(f"average height = {average_height}")

# task 2
# Input a list of student scores
student_scores = input("nput a list of student scores").split()
for n in range(0, len(student_scores)):
    student_scores[n] = int(student_scores[n])


highest_score = 0
for score in student_scores:
    if score > highest_score:
        highest_score = score

# print(highest_score)

print(f"The highest score in the class is: {highest_score}")