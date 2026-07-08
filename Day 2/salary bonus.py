#salary bonus calculator

name = input("Enter Your Name:\n")
salary = int(input("Enter Your Salary:\n$"))
Bonus = int(input("Enter Your Bonus:\n$"))
Bonus_Amount = salary * Bonus / 100
Total_salary = float(salary + Bonus_Amount)
print(f"Hello {name}, Your Total Salary is: ${Total_salary}")