# Correct credentials stored
correct_username = "admin"
correct_password = 12345

# User se input lena
username = input("Enter username: ")
password = input("Enter password: ")

# Dono match hone chahiye tabhi login successful hoga
if username == correct_username and password == correct_password:
    print("✅ Login Successful! Welcome.")
else:
    print("❌ Login Failed! Invalid username or password.")