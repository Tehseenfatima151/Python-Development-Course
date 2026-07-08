name = input("Enter Your Name:\n")
price = int(input("Enter product price:\n$"))
discount = int(input("Enter discount percentage:\n"))
tax = int(input("Enter tax percentage:\n"))
discount_amount = price * discount / 100
final_price = price - discount_amount
tax_amount = final_price * tax / 100
total_price = float(final_price + tax_amount)
print(f"Hello {name}, Your Total Price after discount and tax is: ${total_price}")