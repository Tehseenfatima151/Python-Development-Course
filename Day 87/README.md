# Day 21 – Inheritance, Slicing & Finishing the Snake Game (Part 2)

## 📌 Overview
Is session mein humne **Inheritance** (OOP ka aik advanced concept) aur **Slicing** (lists/strings ka portion nikalna) seekha. Iske baad humne Day 20 wale Snake Game ko **complete** kiya — food/snack add ki (jisse snake grow ho), score tracking banayi, aur collision detection (wall se aur khud ki body se takrana) implement ki.

---

## 1️⃣ What is Inheritance?

**Inheritance** OOP ka ek concept hai jisme ek class (**child class**) doosri class (**parent class**) ki saari properties aur methods **automatically** le leti hai — bina unhe dobara likhe. Isse code **repeat nahi karna parta** (DRY principle).

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")


class Dog(Animal):   # Dog, Animal se inherit kar raha hai
    def bark(self):
        print(f"{self.name} says Woof!")


my_dog = Dog("Rex")
my_dog.eat()    # Output: Rex is eating.  (Animal class ka method, bina dobara likhe)
my_dog.bark()   # Output: Rex says Woof!  (Dog class ka apna naya method)
```

**Explanation:**
- `class Dog(Animal):` — brackets mein parent class ka naam likh kar inheritance set hoti hai
- `Dog` class ne `Animal` ke `__init__` aur `eat()` method **automatically** paa liye
- `Dog` apna khud ka naya method (`bark()`) bhi add kar sakta hai
- Isse **"is-a" relationship** banti hai — Dog **is an** Animal

---

## 2️⃣ Why Inheritance is Useful (Snake Game Context)

Turtle module ki `Turtle` class mein already bohot saari useful properties hain (color, shape, position, movement). Agar humein "Food" ya "Scoreboard" jaisi cheezein banani hain jo **turtle jaisi hi behave karti hain** (screen pe dikhna, position rakhna), to humein `Turtle` class ko **inherit** karna sabse smart tareeqa hai — hume khud se movement/drawing logic likhna nahi parta.

```python
from turtle import Turtle

class Food(Turtle):
    def __init__(self):
        super().__init__()
        # Ab Food class ke paas Turtle ki saari properties hain (shape, color, position waghera)
```

### `super()` Kya Hai?

`super()` parent class ko refer karta hai — `super().__init__()` likhne se parent class ka constructor call hota hai, taake parent ki saari initial setup bhi ho jaye.

```python
class Food(Turtle):
    def __init__(self):
        super().__init__()   # Turtle ka __init__ call hota hai
        self.shape("circle")  # Ab hum Turtle ke methods seedha use kar sakte hain
        self.penup()
```

---

## 3️⃣ What is Slicing?

**Slicing** ka matlab hai list ya string ka ek **portion (hissa)** nikalna, poori cheez ki bajaye.

```python
my_list = [10, 20, 30, 40, 50]

print(my_list[1:4])    # [20, 30, 40] — index 1 se 3 tak
print(my_list[:3])     # [10, 20, 30] — start se index 2 tak
print(my_list[2:])     # [30, 40, 50] — index 2 se end tak
print(my_list[1:])     # [20, 30, 40, 50] — index 1 se end tak (first element chhor kar)
```

**Syntax:** `list[start:end]` — `start` se `end-1` tak elements milte hain (`end` khud include nahi hota).

### Slicing Snake Game Mein Kyun Zaroori Hai

Jab hum check karte hain ke snake ka **head khud ki body se takraya** ya nahi, to head ko khud ke sath compare nahi kar sakte (wo hamesha sach hoga!). Is liye humein **sirf body ke baaki segments** (head chhor kar) check karne hote hain — yahi slicing se hota hai:

```python
for segment in snake.segments[1:]:   # Index 0 (head) chhor kar baaki sab
    if segment.distance(snake.head) < 10:
        print("Collision with tail!")
```

`segments[1:]` — index 1 se lekar end tak sara data deta hai, yani **head (index 0) ko chhor kar** baaki poori body.

---

## 4️⃣ Building the `Food` Class (`food.py`)

```python
from turtle import Turtle
import random


class Food(Turtle):
    """Models a piece of food that appears at random positions for the snake to eat."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Moves the food to a new random position on the screen."""
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
```

**Explanation:**
- `class Food(Turtle):` — Food, Turtle class ko inherit kar rahi hai
- `super().__init__()` — Turtle ka constructor call karta hai, taake Food object ek proper Turtle object ban jaye
- `shapesize()` — turtle ka default size chota kar deta hai (food dot jaisa dikhta hai)
- `refresh()` — food ko naya random position deta hai (jab snake khaye, to naya food yahi method se aayega)

---

## 5️⃣ Building the `Scoreboard` Class (`scoreboard.py`)

```python
from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    """Models the scoreboard that displays and tracks the current score."""

    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears and redraws the current score."""
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """Increases score by 1 and refreshes the display."""
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        """Displays a 'GAME OVER' message in the center of the screen."""
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
```

**Explanation:**
- Scoreboard bhi `Turtle` ko inherit karti hai — isse hum `write()` method use kar ke text screen pe likh sakte hain
- `clear()` phir `write()` — score update karne ka standard tareeqa hai (purana text hata kar naya likhna)
- `increase_score()` snake ke food khane pe call hoga

---

## 6️⃣ Extending `Snake` Class — Growing & Collision Check

Day 20 wali `Snake` class mein humne ab ek naya method add kiya:

```python
def extend(self):
    """Adds a new segment to the snake at the position of the last segment."""
    self.add_segment(self.segments[-1].position())
```

**Explanation:** `segments[-1]` — negative indexing se **aakhri segment** milta hai, aur naya segment usi jagah bana dete hain (agle move pe wo khud automatically follow karega, jaisa Day 20 ke `move()` logic mein dekha tha).

---

## 7️⃣ Collision Detection Logic

### Collision with Food

```python
if snake.head.distance(food) < 15:
    food.refresh()
    snake.extend()
    scoreboard.increase_score()
```

**Explanation:** `distance()` method do turtles ke darmiyan ka fasla nikalta hai — agar wo bohot kam hai (15 pixels se kam), to matlab snake ne food ko "khaya".

### Collision with Wall

```python
if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
    game_is_on = False
    scoreboard.game_over()
```

**Explanation:** Agar snake ke head ki x ya y coordinate screen ki boundary (280) se bahar chali jaye, to game khatam.

### Collision with Own Tail (Slicing Use Hoti Hai Yahan)

```python
for segment in snake.segments[1:]:
    if segment.distance(snake.head) < 10:
        game_is_on = False
        scoreboard.game_over()
```

**Explanation:** Jaisa upar discuss kiya, `segments[1:]` se head ko chhor kar baaki body check hoti hai — agar head kisi bhi baaki segment ke bohot qareeb aa jaye, matlab snake khud se takra gaya.

---

## 8️⃣ Full Combined `main.py`

```python
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=snake.up, key="Up")
screen.onkey(fun=snake.down, key="Down")
screen.onkey(fun=snake.left, key="Left")
screen.onkey(fun=snake.right, key="Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Food collision
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Wall collision
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        game_is_on = False
        scoreboard.game_over()

    # Tail collision (using slicing)
    for segment in snake.segments[1:]:
        if segment.distance(snake.head) < 10:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
```

---

## 9️⃣ Full `snake.py` (Updated with `extend()`)

```python
from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    """Models the snake with multiple body segments that move, turn, and grow."""

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        """Adds a new segment when the snake eats food."""
        self.add_segment(self.segments[-1].position())

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
```

---

## 📸 Screenshot
<img width="1031" height="726" alt="1" src="https://github.com/user-attachments/assets/0fa0906c-ec22-43ef-8a32-9e70bba9a5e6" />

---

## ✅ Key Takeaways
- Inheritance se child class parent class ki properties/methods **bina dobara likhe** le leti hai — `class Child(Parent):` syntax se
- `super().__init__()` parent class ka constructor call karta hai, taake child object properly initialize ho
- Turtle-based custom classes (`Food`, `Scoreboard`) banana asaan hota hai jab `Turtle` ko inherit kiya jaye — sara built-in behavior mil jata hai
- Slicing (`list[start:end]`) list ka koi portion nikalne ke liye use hoti hai — `segments[1:]` se head ko chhor kar baaki body milti hai
- `distance()` method do turtle objects ke darmiyan fasla nikalta hai — collision detection ka core logic
- Poora Snake Game ab **4 classes** (Snake, Food, Scoreboard) + `main.py` mein professionally organized hai — real-world project structure

---

## 🔗 Practice Task
- Game mein "High Score" bhi track karo jo restart ke baad bhi yaad rahe (file mein save kar ke)
- Snake ki speed food khane ke sath thori barhati jao (harder hota jaye game)
- Ek "pause" feature add karo (space key se game pause/resume ho)

---

**🎉 Snake Game Complete!** Ye do-din ka project (Day 20 + Day 21) OOP, event listeners, state, inheritance, aur slicing — sab concepts ka real combination tha, jo ek poora playable game bana kar khatam hua.
