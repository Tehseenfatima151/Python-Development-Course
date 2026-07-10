import random
import string

length = int(input("How long should the password be? "))

characters = string.ascii_letters + string.digits + string.punctuation
password = ""

for i in range(length):
    password += random.choice(characters)

print(f"Your generated password: {password}")