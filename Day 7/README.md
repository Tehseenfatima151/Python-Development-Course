# Day 7 – Hangman Game (Logic Implementation)

## 📌 Overview
Is session mein humne pichle sare concepts (lists, loops, functions, conditionals, randomization, strings) ko combine kar ke ek complete **Hangman Game** banaya. Ye project tha jisme humne word guessing logic, lives tracking, aur game state management ka detailed implementation kiya.

---

## 1️⃣ Game Concept

Hangman ek classic word-guessing game hai:
- Computer random word choose karta hai
- Player ek ek letter guess karta hai
- Agar letter word mein hai → wo sahi jagah show ho jata hai
- Agar letter word mein nahi hai → player ki ek life kam ho jati hai
- Player ki lives khatam hone se pehle agar pura word guess ho jaye → **Win**
- Lives khatam ho jayein aur word complete na ho → **Lose (Game Over)**

---

## 2️⃣ Core Building Blocks Used

Hangman banane ke liye humne ye concepts combine kiye:

| Concept | Kahan Use Hua |
|---------|----------------|
| Lists | Word bank, guessed letters track karna, display list |
| Randomization | `random.choice()` se random word select karna |
| For Loops | Word ke har letter ko check karna |
| While Loops | Game tab tak chalana jab tak win/lose na ho |
| If-Else | Letter sahi hai ya galat check karna |
| Functions | Code ko organized modules mein todna |
| String Methods | Input ko lowercase karna, letters compare karna |

---

## 3️⃣ Step 1: Word Bank & Random Word Selection

```python
import random

word_list = [
    "apple", "banana", "mango", "orange", "grapes",
    "pineapple", "watermelon", "papaya", "guava", "pomegranate",
    "strawberry", "blueberry", "kiwi", "peach", "plum",
    "cherry", "lychee", "apricot", "fig", "coconut",
    "melon", "pear", "banana", "dates", "jackfruit",
    "custard apple", "star fruit", "dragon fruit", "blackberry", "raspberry"
]
chosen_word = random.choice(word_list)

print(chosen_word)   # Debugging ke liye (baad mein hide kar dete hain)
```

`random.choice()` list mein se ek random word select karta hai — har baar game run hone pe alag word aayega.

---

## 4️⃣ Step 2: Blank Display List Banana

Player ko word turant nahi dikhana, is liye har letter ki jagah underscore `"_"` dikhate hain, jitne word ki length hai utne underscores.

```python
word_length = len(chosen_word)
display = []

for _ in range(word_length):
    display.append("_")

print(display)
# Example: ['_', '_', '_', '_', '_', '_']  (agar word "python" hai)
```

---

## 5️⃣ Step 3: Lives Tracking

```python
lives = 6   # Player ko 6 chances milenge
```

Har galat guess pe `lives -= 1` hoga.

---

## 6️⃣ Step 4: Main Game Loop

```python
guessed_letters = []
game_over = False

while not game_over:
    guess = input("Guess a letter: ").lower()

    # Agar letter word mein hai
    if guess in chosen_word:
        for position in range(word_length):
            letter = chosen_word[position]
            if letter == guess:
                display[position] = letter
    else:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            game_over = True
            print("You lose! 😢")

    # Current progress dikhana
    print(" ".join(display))

    # Win condition check
    if "_" not in display:
        game_over = True
        print("You win! 🎉")
```

**Explanation:**
- `guess in chosen_word` — check karta hai ke user ka letter word mein exist karta hai ya nahi
- Agar exist karta hai to `for` loop se **har position** check hoti hai jahan wo letter aata hai (kyunke ek letter word mein multiple baar bhi aa sakta hai, jaise "programming" mein "r" do dafa hai)
- Agar letter exist nahi karta to `lives` kam ho jati hain
- `"_" not in display` — jab display list mein koi underscore baqi nahi bacha, matlab pura word guess ho chuka, player jeet gaya

---

## 7️⃣ Step 5: Preventing Duplicate Guesses (Improvement)

Bina is check ke player baar baar same letter guess kar sakta hai aur bewajah lives waste ho sakti hain:

```python
guessed_letters = []

while not game_over:
    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("You already guessed that letter. Try again.")
        continue

    guessed_letters.append(guess)

    if guess in chosen_word:
        for position in range(word_length):
            if chosen_word[position] == guess:
                display[position] = guess
    else:
        lives -= 1
        if lives == 0:
            game_over = True
            print("You lose! The word was:", chosen_word)

    print(" ".join(display))

    if "_" not in display:
        game_over = True
        print("Congratulations, you win! 🎉")
```

`continue` use kar ke hum current iteration skip kar dete hain agar letter pehle hi guess ho chuka ho — is se lives waste nahi hoti.

---

## 8️⃣ Step 6: Full Combined Logic (Final Version)

```python
import random

word_list = [
    "apple", "banana", "mango", "orange", "grapes",
    "pineapple", "watermelon", "papaya", "guava", "pomegranate",
    "strawberry", "blueberry", "kiwi", "peach", "plum",
    "cherry", "lychee", "apricot", "fig", "coconut",
    "melon", "pear", "banana", "dates", "jackfruit",
    "custard apple", "star fruit", "dragon fruit", "blackberry", "raspberry"
]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

display = ["_"] * word_length
guessed_letters = []
lives = 6
game_over = False

print("Welcome to Hangman!")

while not game_over:
    guess = input("\nGuess a letter: ").lower()

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess in chosen_word:
        for position in range(word_length):
            if chosen_word[position] == guess:
                display[position] = guess
    else:
        print(f"'{guess}' is not in the word.")
        lives -= 1
        print(f"Lives remaining: {lives}")

    print(" ".join(display))

    if "_" not in display:
        print("🎉 You guessed the word! You win!")
        game_over = True

    if lives == 0:
        print(f"💀 Game Over! The word was: {chosen_word}")
        game_over = True
```

---

## 9️⃣ Optional Enhancement: ASCII Art for Lives

Game ko visually interesting banane ke liye hum lives ke sath ek ASCII art stage bhi show kara sakte hain (list of stages, index = lives lost):

```python
stages = ['''
  +---+
  |   |
      |
      |
      |
      |
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
''']

print(stages[lives])
```

Jaise jaise `lives` kam hoti hai, corresponding stage art print hoti jati hai — jitna traditional hangman drawing hota hai.

---

## ✅ Key Takeaways
- Hangman ek complete project hai jo lists, loops, conditionals, functions aur randomization sab ko combine karta hai
- Blank `display` list se word letters ko hide kar ke gradually reveal kiya jata hai
- `for` loop se word ke har position ka letter check karna zaroori hai (multiple occurrences handle karne ke liye)
- `guessed_letters` list duplicate guesses track karti hai
- Win condition: display mein koi underscore na bache
- Lose condition: lives 0 ho jayein
- ASCII art stages se game ko visually engaging banaya ja sakta hai

---

## 🔗 Practice Task
- Word list ko categories mein divide karo (animals, countries, fruits) aur user se category choose karwao
- Score system add karo jo track kare kitne games jeete aur haare
- Hint system add karo jahan player ek extra life ke badle ek letter ka hint le sake
