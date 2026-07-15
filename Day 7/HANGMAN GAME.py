import random
from hangmanstags import stages
from hangmanlogo import logo
from hangmanwords import word_list

logo
chosen_word = random.choice(word_list)
print(f'Pssst, the solution is {chosen_word}.')

display = []
for letter in chosen_word:
    display += "_"
print(display)
lives = 6
while "_" in display and lives > 0:
    guess = input("Guess a letter:").lower()
    if guess in display:
        print(f"You've already guessed {guess}")
    for i in range(len(chosen_word)):
        if chosen_word[i] == guess:
            display[i] = guess
    if guess not in chosen_word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
    print(stages[lives])
print(display)   
if lives == 0:
    print("You lose!")
else:
    print("You win!")
        
