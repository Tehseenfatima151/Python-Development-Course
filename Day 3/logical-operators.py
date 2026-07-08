#Logical Operators
#1.
# and — Dono conditions True hon tabhi result True

age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("You can enter the movie")
else:
    print("Entry denied")

#2.
# or — Agar dono me se koi ek condition True ho to result True
is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("No school today")
else:
    print("School as usual")

#3.
# not — Agar condition True ho to result False aur agar condition False ho to result True
is_raining = False

if not is_raining:
    print("You can go outside")
else:
    print("Take an umbrella")
