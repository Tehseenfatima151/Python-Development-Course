import random
import os
from art import logo, vs

# Data: List of dictionaries containing account info
data = [
    {"name": "Instagram", "follower_count": 346, "description": "Social media platform", "country": "United States"},
    {"name": "Google", "follower_count": 40, "description": "Search engine company", "country": "United States"},
    {"name": "PewDiePie", "follower_count": 111, "description": "YouTuber", "country": "Sweden"},
    {"name": "Cristiano Ronaldo", "follower_count": 215, "description": "Footballer", "country": "Portugal"},
    {"name": "Elon Musk", "follower_count": 128, "description": "Entrepreneur", "country": "United States"},
    {"name": "Selena Gomez", "follower_count": 199, "description": "Singer and actress", "country": "United States"},
    {"name": "The Rock", "follower_count": 334, "description": "Actor and wrestler", "country": "United States"},
    {"name": "Lionel Messi", "follower_count": 246, "description": "Footballer", "country": "Argentina"},
    {"name": "Kim Kardashian", "follower_count": 251, "description": "Media personality", "country": "United States"},
    {"name": "Netflix", "follower_count": 148, "description": "Streaming service", "country": "United States"},
]

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear") 

def get_random_account():
    """Returns a random account dictionary from the data list."""
    return random.choice(data)


def format_data(account):
    """Formats an account dictionary into a readable string."""
    return f"{account['name']}, a {account['description']}, from {account['country']}"


def check_answer(guess, a_follower_count, b_follower_count):
    """Checks whether the user's guess ('a' or 'b') is correct."""
    if a_follower_count > b_follower_count:
        return guess == "a"
    else:
        return guess == "b"


def play_game():
    print(logo)
    score = 0
    game_should_continue = True
    b_account = get_random_account()

    while game_should_continue:
        a_account = b_account
        b_account = get_random_account()
        # Make sure A and B are not the same account
        while a_account == b_account:
            b_account = get_random_account()

        
        print(f"Compare A: {format_data(a_account)}")
        print(vs)
        print(f"Against B: {format_data(b_account)}")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()

        a_follower_count = a_account["follower_count"]
        b_follower_count = b_account["follower_count"]

        is_correct = check_answer(guess, a_follower_count, b_follower_count)

        clear()
        print(logo)
        if is_correct:
            score += 1
            print(f"You're right! Current score: {score}\n")
            
        else:
            game_should_continue = False
            print(f"Sorry, that's wrong. Final score: {score}")



play_game()