# Day 23 – Capstone Project: Turtle Crossing Game

## 📌 Overview
Ye ek **capstone project** tha — jitne bhi Turtle graphics concepts pichle hafte seekhe (event listeners, state, multiple instances, inheritance, slicing, collision detection, OOP structure), sab ek sath combine kar ke ek **Frogger-style crossing game** banaya. Player ko screen ke neeche se upar tak pohanchna hota hai, randomly generate hone wali cars se bachte hue — jitni baar successfully cross kare, level utna barhta hai aur cars utni fast ho jati hain.

---

## 1️⃣ Game Concept

- Player (turtle) screen ke bottom mein start hota hai
- `Up` arrow key se player upar move karta hai
- Cars left se right screen pe randomly generate hoti hain aur move karti hain
- Agar player kisi car se takra jaye → **Game Over**
- Agar player successfully top tak pohanch jaye → **Level Up**, player wapis bottom pe reset hota hai, aur cars ki speed thori barh jati hai

---

## 2️⃣ Project Structure

```
turtle_crossing/
├── main.py
├── player.py
├── car_manager.py
└── scoreboard.py
```

| File | Responsibility |
|------|-----------------|
| `player.py` | `Player` class — movement, position reset, "reached goal" check |
| `car_manager.py` | `CarManager` class — random car generation, movement, speed control |
| `scoreboard.py` | `Scoreboard` class — level tracking, game-over message |
| `main.py` | Screen setup, collision detection, game loop |

---

## 3️⃣ `Player` Class

```python
from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    """Models the player character that moves up the screen, avoiding cars."""

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("white")
        self.penup()
        self.setheading(90)   # Turtle ko shuru se hi "upar" face karwa dete hain
        self.go_to_start()

    def go_to_start(self):
        """Resets the player back to the starting position."""
        self.goto(STARTING_POSITION)

    def move_up(self):
        """Moves the player forward (up) by a fixed distance."""
        self.forward(MOVE_DISTANCE)

    def is_at_finish_line(self):
        """Returns True if the player has reached the top of the screen."""
        return self.ycor() > FINISH_LINE_Y
```

**Explanation:**
- `setheading(90)` — turtle ko 90° (upar) face karwa deta hai, is liye `forward()` call karne se wo hamesha upar hi move karega
- `is_at_finish_line()` — check karta hai ke player ki y-coordinate finish line se aage nikal gayi hai ya nahi

---

## 4️⃣ `CarManager` Class — Random Cars Generate Karna

```python
from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    """Manages the creation, movement, and speed of cars crossing the screen."""

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        """Randomly creates a new car (with a chance-based spawn) on the right side of the screen."""
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        """Moves every car in the list to the left."""
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        """Increases the speed of all future car movement."""
        self.car_speed += MOVE_INCREMENT
```

**Explanation:**
- `create_car()` — `random.randint(1, 6) == 1` se ek **1-in-6 chance** banaya jata hai har frame pe car spawn hone ka — is se cars naturally random intervals pe aati hain, ek sath saari nahi
- `self.all_cars` — ek list jisme sab active car objects store hote hain (jaise Snake ke `segments` list ki tarah)
- `move_cars()` — poori list pe loop chala kar har car ko left move karta hai
- `level_up()` — jab player successfully cross kare, ye method call hota hai aur `car_speed` barha deta hai — is se agli saari cars automatically fast move karengi

---

## 5️⃣ `Scoreboard` Class

```python
from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    """Tracks and displays the current level, and shows a game-over message."""

    def __init__(self):
        super().__init__()
        self.level = 1
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-280, 250)
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears and redraws the current level."""
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        """Increments the level and refreshes the display."""
        self.level += 1
        self.update_scoreboard()

    def game_over(self):
        """Displays a 'GAME OVER' message in the center of the screen."""
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)
```

---

## 6️⃣ Collision Detection Logic

```python
for car in car_manager.all_cars:
    if car.distance(player) < 20:
        game_is_on = False
        scoreboard.game_over()
```

**Explanation:** Har car ke liye check hota hai ke player se uska fasla kitna hai — agar 20 pixels se kam ho jaye, matlab **collision** ho gaya, game khatam.

---

## 7️⃣ Full Combined `main.py`

```python
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move_up, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    # Collision with any car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Player reached the top -> level up
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

screen.exitonclick()
```

**Explanation:**
- Har loop cycle mein: naya car spawn ho sakta hai, sari cars move hoti hain, collision check hota hai, aur finish-line check hota hai
- Jab player top pe pohanch jaye: `go_to_start()` se wapis neeche, `level_up()` se cars fast, `increase_level()` se score update — teeno independent classes ka ek sath coordinate hona (Day 16 wala "objects working together" concept)

---

## 📸 Screenshot

<img width="627" height="662" alt="2" src="https://github.com/user-attachments/assets/0c538d2b-7022-449f-b843-43d6c7848f9e" />
<img width="701" height="693" alt="1" src="https://github.com/user-attachments/assets/4d02463b-0ae4-40e1-a8c8-d599971359c4" />


---

## ✅ Key Takeaways
- Ye capstone project 3 hafton ke concepts ka combination tha: OOP (classes, inheritance), event listeners, state, lists of objects, collision detection (`distance()`), aur randomization
- `CarManager` jaisi "manager" class banana — jo khud koi visible cheez nahi hai, balke doosri cheezon (cars) ko manage karti hai — ek common aur useful design pattern hai
- Randomized spawn chance (`1-in-6`) se naturally distributed events create karna simple lekin effective technique hai
- Progressive difficulty (`car_speed += MOVE_INCREMENT`) ek chhoti si state change se poore game ka feel change kar deta hai
- Teeno classes (`Player`, `CarManager`, `Scoreboard`) completely independent hain, lekin `main.py` unhe coordinate kar ke ek cohesive game banata hai — ye **separation of concerns** ka real-world example hai

---

## 🔗 Practice Task
- Cars ke sath-sath ek **coin/bonus item** add karo jo extra points de
- Level ke sath player ka move-distance bhi thora barhao (extra challenge)
- Ek "Restart" option add karo jo `r` key dabane pe pura game reset kar de (bina program dobara run kiye)
