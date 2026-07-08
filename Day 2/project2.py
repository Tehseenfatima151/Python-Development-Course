#Tip Calculator program 
print("Welcome to the Tip Calculator!")
bill = float(input("What was the total bill? $"))
tip = int(input("How much tip would you like to give? 15, 20, or 30? "))
people = int(input("How many people to split the bill? "))
total_bill = bill + (bill * (tip/100))
bill_per_person = round(total_bill / people,2)
print(f"Each Person should pay: ${bill_per_person}")
