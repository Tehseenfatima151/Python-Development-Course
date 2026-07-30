"""
CLI Blackjack (21) — Pure OOP Implementation
==============================================
Classes: Card, Deck, Hand, Chips, Game

Rules implemented:
- Dynamic Ace value (11 or 1) handling in Hand.get_value()
- Betting system using the Chips class
- Dealer AI: hits until total >= 17
- Robust input validation (no crash on bad input)
- Per-round summary table + end-of-game statistics report
"""

import random
from art import logo


# ======================================================
# 1. CARD CLASS
# ======================================================
class Card:
    """Models a single playing card with a suit and rank."""

    SUITS = ["Hearts", "Diamonds", "Spades", "Clubs"]

    SUIT_SYMBOLS = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Spades": "♠",
        "Clubs": "♣",
    }

    RANKS = {
        "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
        "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
        "Jack": 10, "Queen": 10, "King": 10, "Ace": 11,
    }

    RANK_SHORT = {
        "Two": "2", "Three": "3", "Four": "4", "Five": "5", "Six": "6",
        "Seven": "7", "Eight": "8", "Nine": "9", "Ten": "10",
        "Jack": "J", "Queen": "Q", "King": "K", "Ace": "A",
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.RANKS[rank]

    def __str__(self):
        return f"{Card.RANK_SHORT[self.rank]}{Card.SUIT_SYMBOLS[self.suit]}"


# ======================================================
# 2. DECK CLASS
# ======================================================
class Deck:
    """Models a full 52-card deck. Can be shuffled and dealt from."""

    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        """Generates all 52 cards (13 ranks x 4 suits)."""
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Removes and returns the top card from the deck."""
        if not self.cards:
            # Extremely unlikely in a single game, but rebuild if deck runs out
            self.build_deck()
            self.shuffle()
        return self.cards.pop()


# ======================================================
# 3. HAND CLASS
# ======================================================
class Hand:
    """Models a hand of cards (used for both player and dealer)."""

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def get_value(self):
        """
        Returns the best possible total value of the hand.
        Handles Ace as 11 or 1 dynamically: if total exceeds 21 and
        there is at least one Ace counted as 11, it is converted to 1
        (repeated in a loop to correctly handle multiple Aces).
        """
        total = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == "Ace")

        while total > 21 and num_aces > 0:
            total -= 10   # Convert one Ace from 11 -> 1
            num_aces -= 1

        return total

    def is_bust(self):
        """Returns True if hand value exceeds 21."""
        return self.get_value() > 21

    def is_blackjack(self):
        """Returns True if the hand is a natural 21 with exactly 2 cards."""
        return len(self.cards) == 2 and self.get_value() == 21

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


# ======================================================
# 4. CHIPS CLASS
# ======================================================
class Chips:
    """Models the player's chip balance and betting behavior."""

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def place_bet(self, amount):
        """Deducts the bet amount from the total upfront."""
        self.bet = amount
        self.total -= amount

    def win(self):
        """Player wins: gets back double the bet (original + winnings)."""
        self.total += self.bet * 2

    def lose(self):
        """Player loses: bet was already deducted, nothing more happens."""
        pass

    def push(self):
        """Tie: bet is returned to the player."""
        self.total += self.bet


# ======================================================
# DEALER TURN LOGIC (uses the Hand class)
# ======================================================
def dealer_turn(deck, dealer_hand):
    """Dealer hits until their hand total is 17 or higher."""
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())


# ======================================================
# INPUT VALIDATION HELPERS
# ======================================================
def take_bet(chips):
    """Prompts for a bet amount, validating it's a positive integer within balance."""
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


def hit_or_stand():
    """Prompts the player to hit or stand, validating the input."""
    while True:
        choice = input("Would you like to Hit or Stand? Enter 'h' or 's': ").lower().strip()
        if choice in ("h", "s"):
            return choice
        print("Invalid input. Please enter 'h' for Hit or 's' for Stand.")


def play_again():
    """Asks the player if they want to play another round."""
    while True:
        choice = input("Play another round? Enter 'y' or 'n': ").lower().strip()
        if choice in ("y", "n"):
            return choice == "y"
        print("Invalid input. Please enter 'y' or 'n'.")


# ======================================================
# SUMMARY / REPORTING HELPERS
# ======================================================
def print_summary_table(player_hand, dealer_hand, chips, reveal_dealer=True):
    """Prints a summary table of the current round's state."""
    print("\n" + "-" * 45)
    print(f"{'Round Summary':^45}")
    print("-" * 45)
    print(f"Player Hand   : {player_hand}  (Value: {player_hand.get_value()})")
    if reveal_dealer:
        print(f"Dealer Hand   : {dealer_hand}  (Value: {dealer_hand.get_value()})")
    else:
        hidden_card = dealer_hand.cards[1]
        print(f"Dealer Hand   : {dealer_hand.cards[0]}, ??  (Value: {dealer_hand.cards[0].value}+ hidden)")
    print(f"Current Chips : {chips.total}")
    print("-" * 45 + "\n")


def print_final_report(stats):
    """Prints total rounds played and win/loss/push statistics."""
    print("\n" + "=" * 45)
    print(f"{'GAME OVER — FINAL REPORT':^45}")
    print("=" * 45)
    print(f"Total Rounds Played : {stats['rounds']}")
    print(f"Wins                : {stats['wins']}")
    print(f"Losses              : {stats['losses']}")
    print(f"Pushes (Ties)       : {stats['pushes']}")
    print("=" * 45)


# ======================================================
# MAIN GAME LOOP
# ======================================================
def play_blackjack():
    print(logo)
    print("Welcome to CLI Blackjack!")
    print("Blackjack pays a natural win. Dealer stands on 17 or higher.\n")

    chips = Chips(total=100)
    stats = {"rounds": 0, "wins": 0, "losses": 0, "pushes": 0}

    game_on = True
    while game_on:
        if chips.total <= 0:
            print("You're out of chips! Game Over.")
            break

        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        for _ in range(2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())

        bet_amount = take_bet(chips)
        chips.place_bet(bet_amount)

        print_summary_table(player_hand, dealer_hand, chips, reveal_dealer=False)

        # ---- Player Turn ----
        player_bust = False
        if not player_hand.is_blackjack():
            playing = True
            while playing:
                choice = hit_or_stand()
                if choice == "h":
                    player_hand.add_card(deck.deal_card())
                    print(f"\nPlayer draws: {player_hand.cards[-1]}")
                    print_summary_table(player_hand, dealer_hand, chips, reveal_dealer=False)
                    if player_hand.is_bust():
                        player_bust = True
                        playing = False
                else:
                    playing = False

        # ---- Dealer Turn ----
        if not player_bust and not player_hand.is_blackjack():
            dealer_turn(deck, dealer_hand)

        # ---- Determine Outcome ----
        stats["rounds"] += 1
        player_value = player_hand.get_value()
        dealer_value = dealer_hand.get_value()

        print_summary_table(player_hand, dealer_hand, chips, reveal_dealer=True)

        if player_bust:
            print("You busted! Dealer wins this round.")
            chips.lose()
            stats["losses"] += 1
        elif player_hand.is_blackjack() and not dealer_hand.is_blackjack():
            print("Blackjack! You win this round!")
            chips.win()
            chips.win()  # Blackjack pays extra — simple 2x on top of normal win for a natural 21
            stats["wins"] += 1
        elif dealer_hand.is_bust():
            print("Dealer busted! You win this round!")
            chips.win()
            stats["wins"] += 1
        elif player_value > dealer_value:
            print("You win this round!")
            chips.win()
            stats["wins"] += 1
        elif player_value < dealer_value:
            print("Dealer wins this round.")
            chips.lose()
            stats["losses"] += 1
        else:
            print("Push! It's a tie — your bet is returned.")
            chips.push()
            stats["pushes"] += 1

        print(f"Chips balance: {chips.total}\n")

        if chips.total <= 0:
            print("You're out of chips! Game Over.")
            break

        game_on = play_again()

    print_final_report(stats)


if __name__ == "__main__":
    play_blackjack()