# CLI Blackjack (21) — Pure OOP Implementation

## 📌 Overview
Ek **command-line Blackjack game** jo bilkul pure **Object-Oriented Programming** approach se banaya gaya hai — koi nested dictionaries ya list-based logic use nahi hui, har cheez (Card, Deck, Hand, Chips) apni khud ki class mein encapsulated hai. Ye project real-world OOP design, dynamic Ace-value logic, betting system, dealer AI, aur robust input validation ka combined practical hai.

---

## 🎯 Requirements Checklist

| # | Requirement | Status |
|---|-------------|--------|
| 1 | 4 Classes (Card, Deck, Hand, Chips) — pure OOP | ✅ |
| 2 | `Card` — Suit/Rank store, `__str__` method | ✅ |
| 3 | `Deck` — 52 cards generate, `shuffle()`, `deal_card()` | ✅ |
| 4 | `Hand` — Cards list, `add_card()`, `get_value()` | ✅ |
| 5 | `Chips` — `bet()`, `win()`, `lose()` | ✅ |
| 6 | Dynamic Ace handling (11 → 1 jab total > 21, multiple Aces bhi) | ✅ |
| 7 | Betting system — win pe double, lose pe minus, chips 0 pe Game Over | ✅ |
| 8 | Dealer AI — 17 se kam ho to hit karta rahe | ✅ |
| 9 | Robust input validation — `try-except`, crash nahi hota | ✅ |
| 10 | Round summary table + end-of-game statistics report | ✅ |

---

## 🧱 OOP Structure

```
blackjack_oop.py
├── Card class
├── Deck class
├── Hand class
├── Chips class
├── dealer_turn() function
├── take_bet() / hit_or_stand() / play_again()  — input validation helpers
├── print_summary_table() / print_final_report()
└── play_blackjack()  — main game loop

art.py
└── logo   — ASCII art banner shown at game start
```

---

## 1️⃣ `Card` Class

```python
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.RANKS[rank]

    def __str__(self):
        return f"{Card.RANK_SHORT[self.rank]}{Card.SUIT_SYMBOLS[self.suit]}"
```

**Explanation:** Har card apna suit, rank, aur numeric value store karta hai. `__str__` method se card print hone pe readable format milta hai (jaise `A♠` ya `10♥`), poore dictionary ya tuple ki bajaye.

---

## 2️⃣ `Deck` Class

```python
class Deck:
    def build_deck(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
```

**Explanation:** `build_deck()` list comprehension se 52 `Card` objects banata hai (4 suits × 13 ranks). `deal_card()` list ke aakhir se ek card nikal kar deta hai — is se dealt cards khud-ba-khud deck se remove ho jate hain, koi duplicate dealing nahi hoti.

---

## 3️⃣ `Hand` Class — Ace Ka Dynamic Logic (Sabse Mushkil Part)

```python
def get_value(self):
    total = sum(card.value for card in self.cards)
    num_aces = sum(1 for card in self.cards if card.rank == "Ace")

    while total > 21 and num_aces > 0:
        total -= 10
        num_aces -= 1

    return total
```

**Explanation:**
- Har Ace **initially 11** ki value rakhta hai
- Agar total 21 se cross ho jaye AUR hand mein koi Ace hai jo abhi 11 count ho raha hai, to us Ace ki value **10 kam kar dete hain** (11 → 1)
- Ye **`while` loop mein** hota hai, is liye **multiple Aces** bhi sahi handle hote hain — e.g. 2 Aces + 9 = pehle 31 (bust) → loop chalta hai → 21 (perfect)

**Tested cases:**
```
Two Aces + 9        → 21  ✅ (dono Aces smartly 1+1+9+... adjust hote hain)
Ace + King           → 21  ✅ (Blackjack detect hota hai)
Ace + 5 + 8           → 14  ✅ (Ace khud 1 ban jata hai, warna 24 bust hota)
```

---

## 4️⃣ `Chips` Class

```python
class Chips:
    def place_bet(self, amount):
        self.bet = amount
        self.total -= amount

    def win(self):
        self.total += self.bet * 2

    def lose(self):
        pass   # bet already deduct ho chuka hai

    def push(self):
        self.total += self.bet   # tie pe bet wapis
```

**Explanation:** Bet lagate hi turant chips se minus ho jati hai (`place_bet`). Jeetne pe original bet + jeet dono wapis milti hai (`bet * 2`). Harne pe kuch nahi hota (already deduct ho chuki). Tie (push) pe sirf bet wapis mil jati hai.

---

## 5️⃣ Dealer AI Logic

```python
def dealer_turn(deck, dealer_hand):
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
```

**Explanation:** Ye standalone function `Hand` class ko use karta hai — dealer tab tak cards leta rehta hai jab tak uska total 17 se kam hai, jaisa real casino rule hota hai.

---

## 6️⃣ Robust Input Validation

```python
def take_bet(chips):
    while True:
        try:
            amount = int(input(f"You have {chips.total} chips. How many would you like to bet?: "))
        except ValueError:
            print("Sorry, please enter a whole number for your bet.")
            continue

        if amount <= 0:
            print("Bet must be greater than zero.")
        elif amount > chips.total:
            print("Sorry, your bet cannot exceed your available chips.")
        else:
            return amount
```

**Explanation:** `try-except ValueError` catch karta hai agar user ne number ki jagah text (jaise `"abc"`) likha ho — program crash nahi hota, sirf error message de kar dobara input mangta hai. Isi pattern se `hit_or_stand()` aur `play_again()` bhi non-crashing hain.

---

## 7️⃣ Summary Table & Final Report

```python
def print_summary_table(player_hand, dealer_hand, chips, reveal_dealer=True):
    print(f"Player Hand   : {player_hand}  (Value: {player_hand.get_value()})")
    print(f"Dealer Hand   : {dealer_hand}  (Value: {dealer_hand.get_value()})")
    print(f"Current Chips : {chips.total}")
```

Har round ke baad ye table print hoti hai. Game khatam hone pe:

```python
def print_final_report(stats):
    print(f"Total Rounds Played : {stats['rounds']}")
    print(f"Wins                : {stats['wins']}")
    print(f"Losses              : {stats['losses']}")
    print(f"Pushes (Ties)       : {stats['pushes']}")
```

---

## 🎨 ASCII Art Logo (`art.py`)

Game shuru hone pe ek local `art.py` file se `logo` import ki jati hai — do playing cards (Ace of Spades, King of Hearts) ka design "BLACKJACK" title ke sath.

```python
from art import logo
print(logo)
```

⚠️ **Zaroori:** `art.py` aur `blackjack_oop.py` **dono ek hi folder mein** hone chahiye, kyunke `art.py` koi Python package nahi — ye is project ki apni local file hai.

---

## ▶️ How to Run

```bash
python blackjack_oop.py
```

**Controls:**
- Bet amount: koi bhi number type karo (chips balance se zyada nahi)
- `h` — Hit (naya card lo)
- `s` — Stand (rukh jao)
- `y`/`n` — agla round khelna hai ya nahi

---

## 📸 Screenshot

<img width="1363" height="728" alt="ss" src="https://github.com/user-attachments/assets/23b19980-7a11-4445-8b86-d2955a4428bc" />

---

## ✅ Key Takeaways
- Poora game **4 classes** mein cleanly organized hai — koi global state ya nested dictionaries nahi
- Dynamic Ace logic `while` loop se elegantly handle hoti hai — multiple Aces bhi sahi resolve hote hain
- Betting flow (`place_bet → win/lose/push`) chips ko kabhi negative ya inconsistent nahi hone deta
- `dealer_turn()` ek standalone function hai jo `Hand` class use karta hai — separation of concerns achi tarah maintained hai
- Har input validation loop (`try-except` + `while True`) program ko crash-proof banata hai
- Local `art.py` file se ASCII banner import karna presentation ko professional touch deta hai

---

## 🔗 Practice Task
- Split feature add karo (agar player ke pehle 2 cards same value ke hon, to hand split kar sake)
- Insurance bet add karo jab dealer ka pehla card Ace ho
- Game statistics ko ek `.txt` ya `.json` file mein save karo taake sessions ke beech persist rahein
