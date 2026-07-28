# Day 16 – Object-Oriented Programming (OOP) & Coffee Machine (OOP Version)

## 📌 Overview
Is session mein humne **Object-Oriented Programming (OOP)** ka detailed concept seekha — classes, objects, attributes, methods, aur encapsulation kya hote hain. Iske baad humne Day 15 wale Coffee Machine program ko **OOP style mein rewrite** kiya — is dafa code alag alag classes aur alag alag files mein organized kiya, jo real-world professional Python projects ka standard tareeqa hai.

---

## 1️⃣ What is OOP (Object-Oriented Programming)?

OOP ek programming paradigm hai jisme code ko **objects** ke around organize kiya jata hai — har object apne data (attributes) aur apne functions (methods) rakhta hai. Ye real-world cheezon ko code mein model karne ka natural tareeqa hai.

**Procedural vs OOP:**

| Procedural (Day 15 wala style) | OOP (Day 16 wala style) |
|--------------------------------|--------------------------|
| Functions aur global variables alag hote hain | Data aur functions ek object ke andar bundled hote hain |
| `resources = {...}` alag, `make_coffee()` alag | `CoffeeMaker` class apne resources khud rakhti hai aur khud drink banati hai |
| Code ek hi file mein hota hai | Code multiple files/classes mein organized hota hai |

---

## 2️⃣ Class & Object

**Class** ek blueprint/template hoti hai. **Object** us blueprint se banaya gaya actual instance hota hai.

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def honk(self):
        print(f"{self.brand} says beep beep!")

my_car = Car("Toyota", "White")   # Object banana (instance)
my_car.honk()                      # Output: Toyota says beep beep!
```

**Explanation:**
- `class Car:` — blueprint define karta hai
- `__init__()` — **constructor** method hai, jab bhi naya object banta hai ye automatically call hota hai, initial values set karne ke liye
- `self` — object khud ko refer karta hai (current instance)
- `my_car = Car(...)` — ek naya object (instance) banaya
- `my_car.honk()` — object ka method call kiya

---

## 3️⃣ Attributes & Methods

- **Attributes** — object ki properties/data (jaise `brand`, `color`)
- **Methods** — object ke functions (jaise `honk()`)

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")


account = BankAccount("Ali", 1000)
account.deposit(500)     # Deposited $500. New balance: $1500
account.withdraw(2000)   # Insufficient funds!
```

---

## 4️⃣ Encapsulation

**Encapsulation** ka matlab hai data (attributes) ko object ke andar "wrap" kar dena, aur usse sirf uske apne methods ke through access/modify karna — bahar se seedha chhairna nahi. Isse data safe rehta hai aur galti se corrupt nahi hota.

```python
class CoffeeMaker:
    def __init__(self):
        self.water = 300   # Ye attribute class ke andar "encapsulated" hai

    def use_water(self, amount):
        if amount <= self.water:
            self.water -= amount
        else:
            print("Not enough water!")


machine = CoffeeMaker()
machine.use_water(50)      # Sahi tareeqa — method ke through modify karna
print(machine.water)        # Output: 250
```

Encapsulation ki wajah se hum `machine.water = -500` jaisi galti se bachte hain — sirf `use_water()` method hi water ki value ko controlled tareeqe se change kar sakta hai.

---

## 5️⃣ Multiple Files / Modules (Professional Project Structure)

Bare projects mein har class apni alag `.py` file mein rakhi jati hai, aur `main.py` unhe **import** kar ke use karta hai. Ye code ko organized aur reusable banata hai.

```
coffee_machine_oop/
├── main.py
├── menu.py
├── coffee_maker.py
└── money_machine.py
```

---

## 6️⃣ Designing the Coffee Machine with OOP

Humne Coffee Machine ko **4 classes** mein divide kiya, har class ki apni responsibility hai:

| Class | File | Responsibility |
|-------|------|-----------------|
| `MenuItem` | `menu.py` | Ek single drink (name, cost, ingredients) represent karta hai |
| `Menu` | `menu.py` | Sare drinks ki list rakhta hai, drink dhoondne ka method deta hai |
| `CoffeeMaker` | `coffee_maker.py` | Resources (water, milk, coffee) track karta hai, sufficiency check karta hai, drink banata hai |
| `MoneyMachine` | `money_machine.py` | Coins process karta hai, profit track karta hai, transaction verify karta hai |

---

## 7️⃣ `menu.py` — MenuItem & Menu Classes

```python
class MenuItem:
    """Models each Menu Item with a name, cost, and required ingredients."""

    def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee,
        }


class Menu:
    """Models the Menu with a list of MenuItem objects."""

    def __init__(self):
        self.menu = [
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem(name="cappuccino", water=250, milk=100, coffee=24, cost=3.0),
        ]

    def get_items(self):
        """Returns all the names of the available menu items as a string."""
        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options

    def find_drink(self, order_name):
        """Searches the menu for a particular drink by name, returns MenuItem object or None."""
        for item in self.menu:
            if item.name == order_name:
                return item
        print("Sorry that item is not available.")
        return None
```

---

## 8️⃣ `coffee_maker.py` — CoffeeMaker Class

```python
class CoffeeMaker:
    """Models the machine that makes the coffee."""

    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    def report(self):
        """Prints a report of all resources."""
        print(f"Water: {self.resources['water']}ml")
        print(f"Milk: {self.resources['milk']}ml")
        print(f"Coffee: {self.resources['coffee']}g")

    def is_resource_sufficient(self, drink):
        """Returns True when order can be made, False if ingredients are insufficient."""
        can_make = True
        for item in drink.ingredients:
            if drink.ingredients[item] > self.resources[item]:
                print(f"Sorry there is not enough {item}.")
                can_make = False
        return can_make

    def make_coffee(self, order):
        """Deducts the required ingredients from the resources."""
        for item in order.ingredients:
            self.resources[item] -= order.ingredients[item]
        print(f"Here is your {order.name}. Enjoy!")
```

---

## 9️⃣ `money_machine.py` — MoneyMachine Class

```python
class MoneyMachine:
    """Models the machine that processes coins and transactions."""

    CURRENCY = "$"

    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01,
    }

    def __init__(self):
        self.profit = 0
        self.money_received = 0

    def report(self):
        """Prints the current profit."""
        print(f"Money: {self.CURRENCY}{self.profit}")

    def process_coins(self):
        """Returns the total calculated from coins inserted."""
        print("Please insert coins.")
        for coin in self.COIN_VALUES:
            self.money_received += int(input(f"How many {coin}?: ")) * self.COIN_VALUES[coin]
        return self.money_received

    def make_payment(self, cost):
        """Checks if payment is sufficient, returns True/False, gives change if needed."""
        self.process_coins()
        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            print(f"Here is {self.CURRENCY}{change} in change.")
            self.profit += cost
            self.money_received = 0
            return True
        else:
            print("Sorry that's not enough money. Money refunded.")
            self.money_received = 0
            return False
```

---

## 🔟 `main.py` — Bringing It All Together

```python
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()

is_on = True

while is_on:
    options = menu.get_items()
    choice = input(f"What would you like? ({options}): ").lower()

    if choice == "off":
        is_on = False
        print("Turning off the coffee machine. Goodbye!")

    elif choice == "report":
        coffee_maker.report()
        money_machine.report()

    else:
        drink = menu.find_drink(choice)
        if drink is not None:
            if coffee_maker.is_resource_sufficient(drink):
                if money_machine.make_payment(drink.cost):
                    coffee_maker.make_coffee(drink)
```

**Explanation:**
- `main.py` sirf **objects banata hai** aur unke methods ko coordinate karta hai — asal logic har class ke andar hai
- `menu.find_drink(choice)` — Menu class se drink object dhoondte hain
- `coffee_maker.is_resource_sufficient(drink)` — CoffeeMaker khud apne resources check karta hai
- `money_machine.make_payment(drink.cost)` — MoneyMachine khud coins process aur transaction verify karta hai
- `coffee_maker.make_coffee(drink)` — sirf tab call hota hai jab resources aur payment dono sahi hon

---

## 1️⃣1️⃣ Example Run

```
What would you like? (espresso/latte/cappuccino/): latte
Please insert coins.
How many quarters?: 10
How many dimes?: 0
How many nickles?: 0
How many pennies?: 0
Here is $0.0 in change.
Here is your latte. Enjoy!

What would you like? (espresso/latte/cappuccino/): report
Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.5
```
## 1️⃣2️⃣ Screenshoot
<img width="1366" height="732" alt="coffe machine" src="https://github.com/user-attachments/assets/cba913a6-5d12-40d8-af67-766702a433de" />

---

## ✅ Key Takeaways
- OOP data aur behavior ko object ke andar bundle karta hai, jisse code real-world entities jaisa organize hota hai
- Class blueprint hoti hai, object us blueprint se bana instance hota hai
- `__init__()` constructor hai jo object banate hi automatically chalta hai
- `self` current object ko refer karta hai, har method ka pehla parameter hota hai
- Encapsulation data ko safe rakhta hai — sirf class ke apne methods se modify hota hai
- Bare projects ko multiple files (`menu.py`, `coffee_maker.py`, etc.) mein split karna aur `import` karna professional practice hai
- Procedural code (Day 15) aur OOP code (Day 16) same kaam karte hain, lekin OOP zyada scalable, organized, aur maintainable hota hai — especially jab project bara ho jaye

---

## 🔗 Practice Task
- `MenuItem` class mein ek naya attribute add karo jaisay `calories`, aur report mein use bhi show karo
- `CoffeeMaker` class mein ek `refill()` method add karo jo sare resources ko wapis full kar de
- Poora project GitHub pe multiple files ke sath push karo — `main.py`, `menu.py`, `coffee_maker.py`, `money_machine.py` alag alag
