from art import logo


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
    print(f"Here is your {drink_name}☕. Enjoy!")


def run_coffee_machine():
    is_on = True
    print(logo)
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


if __name__ == "__main__":
    run_coffee_machine()