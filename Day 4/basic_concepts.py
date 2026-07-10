# Useful List Functions
import random


numbers = [5, 3, 8, 1, 9]

print(len(numbers))     # List ki length -> 5
print(max(numbers))     # Sabse bara number -> 9
print(min(numbers))     # Sabse chota number -> 1
print(sum(numbers))     # Sab ka sum -> 26

numbers.sort()           # Ascending order
print(numbers)           # [1, 3, 5, 8, 9]

numbers.reverse()        # List ko ulta karna
print(numbers)           # [9, 8, 5, 3, 1]

# random.choice() — List se random element choose karna
colors = ["red", "blue", "green", "yellow"]
picked = random.choice(colors)
print(picked)   # List mein se koi bhi ek random color

# random.shuffle() — List ko shuffle (mix) karna

cards = ["A", "K", "Q", "J", "10"]
random.shuffle(cards)
print(cards)   # Order har dafa alag hoga