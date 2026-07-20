import random
from art import logo
easy_level = 10
hard_level = 5 

def choose_level():
    choose_level = input("Choose a difficulty. Type 'easy' or 'hard':")
    if choose_level == "easy" :
        return easy_level
    elif choose_level == "hard" :
        return hard_level  
 

def num_guess(guess, number, attempts):                       
    
    if guess > number:
        print("Too high.")
        return attempts - 1

    elif guess < number:
        print("Too low.")
        return attempts - 1
    else:
        print(f"You got it! The answer was {number}.")

def game():
    print(logo)
    print("Welcome to the Number Guessing Game!")
    print("I am thinking of a Number between 1 and 100.")
    number = random.randint(1, 100)
    print(f"Pssst, the correct answer is {number}")
    attempts = choose_level() 
    guess = 0

    while guess!= number:
            print(f"You have {attempts} attempts remaining to guess a number. ")
            guess=int(input("Make a guess:"))
            attempts = num_guess(guess, number, attempts)
            if attempts == 0:
                print("You've run out of guesses, you lose.")
                return
            elif guess != number:
                print("Guess again.")

game()

