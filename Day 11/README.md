# Day 11 – Blackjack Game (Capstone Project)

## 📌 Overview
Is session mein humne ek complete **Blackjack Card Game** banaya jo is bootcamp ke pehle 10 din mein seekhe gaye tamam basic Python concepts ka combination tha — variables, data types, lists, functions, loops, conditionals, randomization, aur dictionaries sab ek real project mein use huay. Ye ab tak ka sabse bara aur complete logic implementation tha.

---

## 1️⃣ Game Rules (Blackjack Basics)

Blackjack ek card game hai jisme:
- Player aur Computer (dealer) dono ko 2-2 cards milti hain
- Cards ki value: Number cards apni value ke barabar, Jack/Queen/King = 11 (yahan simplified rules mein), Ace = 11 ya 1 (jo bhi better ho)
- Player aur dealer ke cards ka total **21** ke jitna qareeb hona chahiye
- 21 se zyada ho jaye to **"Bust"** (haar)
- Pehli 2 cards se exact 21 ban jaye to **"Blackjack"** (fori jeet)
- Jo bhi 21 ke zyada qareeb ho bina bust huay, wo jeet jata hai

---

## 2️⃣ Concepts Combined in This Project

| Concept | Kahan Use Hua |
|---------|----------------|
| Lists | Deck of cards, player hand, computer hand |
| Randomization | `random.choice()` se random card nikalna |
| Functions | Card dealing, score calculation, game logic ko modules mein todna |
| While Loops | Game ko chalate rehna jab tak bust/stand na ho |
| If-Elif-Else | Bust, blackjack, win/lose/draw conditions check karna |
| Dictionaries/Data | Card values ko organize karna |
| String Formatting (f-strings) | Cards aur scores ko readable tareeqe se show karna |
| Functions with Return | Score calculate kar ke wapis bhejna |

---

## 3️⃣ Step 1: Creating the Deck of Cards

```python
import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# 11 = Ace, 10 = Jack/Queen/King, baqi apni values ke barabar
```

`random.choice(cards)` har baar deck se ek random card nikalega (yahan deck infinite maan rahe hain, jaisay real casino shoe mein hota hai).

---

## 4️⃣ Step 2: Dealing Cards Function

```python
def deal_card():
    """Returns a random card from the deck."""
    return random.choice(cards)
```

Player aur computer dono ko shuru mein 2-2 cards deni hoti hain:

```python
player_cards = []
computer_cards = []

for _ in range(2):
    player_cards.append(deal_card())
    computer_cards.append(deal_card())
```

---

## 5️⃣ Step 3: Calculating the Score

Ye function list of cards leta hai aur unka total sum nikalta hai — lekin Ace (11) aur Blackjack ka special handling bhi karta hai.

```python
def calculate_score(cards):
    """Takes a list of cards and returns the score, handling Ace and Blackjack rules."""
    
    if sum(cards) == 21 and len(cards) == 2:
        return 0   # Blackjack! (0 ek special signal hai)

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)   # Ace ko 11 ki bajaye 1 count karo

    return sum(cards)
```

**Explanation:**
- Agar sirf 2 cards mein hi total 21 ho jaye → ye **Blackjack** hai, `0` return karte hain (jisse baad mein special message dikhaya jata hai)
- Agar hand mein Ace (11) hai aur total 21 se upar chala gaya hai, to Ace ki value 11 se 1 kar dete hain (real Blackjack rule) taake bust hone se bacha ja sake
- Warna simple `sum()` return kar dete hain

---

## 6️⃣ Step 4: Comparing Scores (Winner Decide Karna)

```python
def compare(user_score, computer_score):
    """Compares scores and returns the result message."""
    
    if user_score == computer_score:
        return "Draw 🙃"
    elif computer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif computer_score > 21:
        return "Opponent went over. You win 😁"
    elif user_score > computer_score:
        return "You win 😃"
    else:
        return "You lose 😤"
```

Ye function comparison ka pura logic ek jagah handle karta hai — is se main game loop clean rehta hai.

---

## 7️⃣ Step 5: Main Game Loop

```python
def play_game():
    print("Welcome to Blackjack!")

    player_cards = []
    computer_cards = []
    is_game_over = False

    # Shuru mein 2-2 cards dena
    for _ in range(2):
        player_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        player_score = calculate_score(player_cards)
        computer_score = calculate_score(computer_cards)

        print(f"Your cards: {player_cards}, current score: {player_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        # Blackjack ya bust ho gaya to game khatam
        if player_score == 0 or computer_score == 0 or player_score > 21:
            is_game_over = True
        else:
            should_deal_more = input("Type 'y' to get another card, 'n' to pass: ").lower()
            if should_deal_more == "y":
                player_cards.append(deal_card())
            else:
                is_game_over = True

    # Computer ka logic: agar score 17 se kam hai to card leta rahega (standard casino rule)
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"Your final hand: {player_cards}, final score: {player_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(player_score, computer_score))
```

---

## 8️⃣ Step 6: Full Combined Program

```python
import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card():
    """Returns a random card from the deck."""
    return random.choice(cards)


def calculate_score(cards):
    """Takes a list of cards and returns the score, handling Ace and Blackjack rules."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)


def compare(user_score, computer_score):
    """Compares scores and returns the result message."""
    if user_score == computer_score:
        return "Draw 🙃"
    elif computer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif computer_score > 21:
        return "Opponent went over. You win 😁"
    elif user_score > computer_score:
        return "You win 😃"
    else:
        return "You lose 😤"


def play_game():
    print("Welcome to Blackjack!")

    player_cards = []
    computer_cards = []
    is_game_over = False

    for _ in range(2):
        player_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        player_score = calculate_score(player_cards)
        computer_score = calculate_score(computer_cards)

        print(f"Your cards: {player_cards}, current score: {player_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if player_score == 0 or computer_score == 0 or player_score > 21:
            is_game_over = True
        else:
            should_deal_more = input("Type 'y' to get another card, 'n' to pass: ").lower()
            if should_deal_more == "y":
                player_cards.append(deal_card())
            else:
                is_game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"Your final hand: {player_cards}, final score: {player_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(player_score, computer_score))


should_play = True
while should_play:
    play_game()
    again = input("\nDo you want to play again? Type 'y' or 'n': ").lower()
    if again == "n":
        should_play = False
        print("Thanks for playing!")
```

---

## 9️⃣ Example Run

```
Welcome to Blackjack!
Your cards: [10, 7], current score: 17
Computer's first card: 9
Type 'y' to get another card, 'n' to pass: n

Your final hand: [10, 7], final score: 17
Computer's final hand: [9, 10, 3], final score: 22
Opponent went over. You win 😁
```

---

## ✅ Key Takeaways
- Blackjack ek capstone project tha jo saare basic concepts (lists, functions, loops, conditionals, randomization) ek jagah combine karta hai
- Card dealing, score calculation, aur comparison — teeno kaam ko alag alag functions mein todna code ko readable aur debuggable banata hai
- Real-world rules (jaise Ace ki dual value: 11 ya 1) ko code mein handle karna important logic-building skill hai
- `0` jaisi special value use kar ke Blackjack ka signal dena aik smart trick hai bina extra variable use kiye
- Computer ka "17 tak card leta rahe" rule real casino logic follow karta hai — ye AI jaisa simple decision-making dikhata hai
- Poora game outer `while` loop mein wrap kiya gaya taake multiple rounds khela ja sake

---

## 🔗 Practice Task
- Game mein multiple players add karo (2 ya zyada players ek sath khel sakein)
- Betting system add karo jahan har round pe player apne "coins" pe bet lagaye
- Card counting feature add karo jo track kare ke ab tak kitne high/low cards nikal chuke hain
