# Day 15 – Coffee Machine Program

## 📌 Overview
Is session mein humne ek complete **Coffee Machine simulator** banaya jo real vending machine ki tarah kaam karta hai — drink select karna, resources (water, milk, coffee) check karna, coins process karna, transaction verify karna, change dena, aur report generate karna. Ye project pichle sessions ke concepts — dictionaries, functions, conditionals, loops, aur nested data structures — ka practical, real-world combination tha.

---

## 1️⃣ Program Requirements (Summary)

| # | Requirement |
|---|-------------|
| 1 | User se drink poochna (espresso/latte/cappuccino), har action ke baad prompt dobara show ho |
| 2 | "off" type karne se machine band ho jaye (program end) |
| 3 | "report" type karne se current resources dikhein |
| 4 | Drink banane se pehle resources sufficient hain ya nahi check karna |
| 5 | Coins process karna (quarters, dimes, nickels, pennies) |
| 6 | Transaction successful hai ya nahi check karna, kam paise pe refund, zyada pe change |
| 7 | Coffee banana — resources deduct karna aur drink serve karna |

---

## 2️⃣ Concepts Used in This Project

| Concept | Kahan Use Hua |
|---------|----------------|
| Dictionaries & Nesting | Menu items (ingredients + cost), machine resources |
| Functions with Return | Resource check, coin processing, transaction check, coffee making |
| While Loop | Machine ko continuously chalate rehna jab tak "off" na aaye |
| If-Elif-Else | Drink choice handle karna, resource aur money check karna |
| Boolean Flags | Machine ki `is_on` state track karna |
| f-Strings | Report aur messages format karna |

---

## 3️⃣ Step 1: Data Setup (Menu & Resources)

```python
MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0
```

**Explanation:**
- `MENU` ek dictionary hai jisme har drink khud ek dictionary hai (nesting), jisme `ingredients` aur `cost` store hote hain
- `resources` current machine ki available quantities track karta hai
- `profit` machine mein jama hua paisa track karta hai

---

## 4️⃣ Step 2: Resource Check Function (Requirement 4)

```python
def is_resource_sufficient(order_ingredients):
    """Returns True if there are enough resources to make the drink, False otherwise."""
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True
```

**Explanation:**
- Har ingredient (jaise water, milk, coffee) ko required amount se compare karta hai
- Agar koi bhi ingredient kam pare, to specific message print hota hai (e.g. "not enough water") aur `False` return hota hai

---

## 5️⃣ Step 3: Process Coins Function (Requirement 5)

```python
def process_coins():
    """Prompts user to insert coins and returns the total calculated value."""
    print("Please insert coins.")
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))

    total = (quarters * 0.25) + (dimes * 0.10) + (nickles * 0.05) + (pennies * 0.01)
    return total
```

**Explanation:**
- Har coin type ki quantity input se li jati hai
- Total value calculate ki jati hai — quarters = $0.25, dimes = $0.10, nickels = $0.05, pennies = $0.01

---

## 6️⃣ Step 4: Transaction Check Function (Requirement 6)

```python
def is_transaction_successful(money_received, drink_cost):
    """Checks if payment is sufficient. Returns True and gives change if needed, False if insufficient."""
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        if change > 0:
            print(f"Here is ${change} in change.")
        global profit
        profit += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False
```

**Explanation:**
- Agar paisa cost se zyada ya barabar hai → transaction successful, agar extra paisa hai to change round kar ke diya jata hai (`round(..., 2)`)
- Successful transaction pe `profit` (global variable) mein drink ki cost add ho jati hai
- Agar paisa kam hai → refund message aur `False` return

---

## 7️⃣ Step 5: Make Coffee Function (Requirement 7)

```python
def make_coffee(drink_name, order_ingredients):
    """Deducts the required ingredients from resources and serves the drink."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name}. Enjoy!")
```

**Explanation:**
- Har ingredient jo drink ke liye chahiye tha, use `resources` dictionary se minus kar diya jata hai
- Aakhir mein serving message print hota hai

---

## 8️⃣ Step 6: Report Function (Requirement 3)

```python
def print_report():
    """Prints the current resource levels and profit."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")
```

---

## 9️⃣ Step 7: Main Program Loop (Requirements 1 & 2)

```python
is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if choice == "off":
        is_on = False
        print("Turning off the coffee machine. Goodbye!")

    elif choice == "report":
        print_report()

    elif choice in MENU:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])

    else:
        print("Sorry, that's not a valid option. Please try again.")
```

**Explanation:**
- `while is_on` — machine tab tak chalti hai jab tak `is_on` `False` na ho jaye ("off" type karne se)
- `"report"` type karne se resources ka current status show ho jata hai
- Agar valid drink choose ho, to sequence chalta hai: **resource check → coin processing → transaction check → coffee making**
- Har action complete hone ke baad loop wapis shuru se chalta hai, aur naya prompt show hota hai (next customer ke liye)

---

## 🔟 Full Combined Program

```python
MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0


def print_report():
    """Prints the current resource levels and profit."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")


def is_resource_sufficient(order_ingredients):
    """Returns True if there are enough resources to make the drink, False otherwise."""
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True


def process_coins():
    """Prompts user to insert coins and returns the total calculated value."""
    print("Please insert coins.")
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))

    total = (quarters * 0.25) + (dimes * 0.10) + (nickles * 0.05) + (pennies * 0.01)
    return total


def is_transaction_successful(money_received, drink_cost):
    """Checks if payment is sufficient. Returns True and gives change if needed, False if insufficient."""
    global profit
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        if change > 0:
            print(f"Here is ${change} in change.")
        profit += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False


def make_coffee(drink_name, order_ingredients):
    """Deducts the required ingredients from resources and serves the drink."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name}. Enjoy!")


is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if choice == "off":
        is_on = False
        print("Turning off the coffee machine. Goodbye!")

    elif choice == "report":
        print_report()

    elif choice in MENU:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])

    else:
        print("Sorry, that's not a valid option. Please try again.")
```
## 1️⃣2️⃣ Screenshoot
<img width="1205" height="730" alt="coffee" src="https://github.com/user-attachments/assets/ce69fe90-0a6f-49aa-b703-dadc9ba61386" />

---

## 1️⃣1️⃣ Example Run

```
What would you like? (espresso/latte/cappuccino): latte
Please insert coins.
How many quarters?: 6
How many dimes?: 5
How many nickles?: 0
How many pennies?: 0
Here is $0.5 in change.
Here is your latte. Enjoy!

What would you like? (espresso/latte/cappuccino): report
Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.5

What would you like? (espresso/latte/cappuccino): cappuccino
Sorry there is not enough milk.

What would you like? (espresso/latte/cappuccino): off
Turning off the coffee machine. Goodbye!
```

---

## ✅ Key Takeaways
- Nested dictionaries real-world menu systems (item → ingredients + price) modeling ka natural tareeqa hain
- Har responsibility (resource check, coin processing, transaction check, making coffee, reporting) ko alag function mein rakhna code ko readable aur maintainable banata hai
- `global` keyword yahan `profit` update karne ke liye zaroori tha kyunke wo function ke bahar define tha aur multiple functions se update hona tha
- `round(value, 2)` se currency values ko hamesha 2 decimal places tak rakha jata hai (real-world money handling)
- Loop-based menu systems (`while is_on`) real vending machines/POS systems ka basic structure hain
- Special keywords (`"off"`, `"report"`) normal menu choices se pehle check karna zaroori hai, warna wo galti se drink options samjhe ja sakte hain

---

## 🔗 Practice Task
- Machine mein ek naya drink add karo (jaisay "mocha") apni khud ki ingredients aur cost ke sath
- Resources ko refill karne ka ek admin option add karo (jaisay "refill" command)
- Coin count ko bhi track karo aur report mein total coins inserted bhi show karo
