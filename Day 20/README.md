# Day 20 – Snake Game (Part 1: Snake Body, Movement & Direction Control)

## 📌 Overview
Is session mein humne classic **Snake Game** banana shuru kiya — Part 1 mein humne **snake ka body banaya** (multiple turtle segments se), usse **move karwaya**, aur **keyboard se direction control** implement ki (bina ulti direction mein jaane ke, jaise real Snake game mein hota hai). Ye project OOP (Day 16-17), event listeners (Day 19), aur lists ka combined practical use tha.

---

## 1️⃣ Project Structure (Multiple Files)

Professional practice follow karte hue, humne code ko files mein divide kiya:

```
snake_game/
├── main.py
└── snake.py
```

| File | Responsibility |
|------|-----------------|
| `snake.py` | `Snake` class — body banana, move karna, direction change karna |
| `main.py` | Screen setup, event listeners bind karna, game loop chalana |

---

## 2️⃣ Setting Up the Screen (`main.py` — Initial Version)

```python
from turtle import Screen
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)   # Screen ki auto-update band karo, hum khud control karenge

game_is_on = True
while game_is_on:
    screen.update()   # Screen ko manually refresh karo
    time.sleep(0.1)    # Har refresh ke darmiyan thora delay

screen.exitonclick()
```

**Explanation:**
- `screen.tracer(0)` — Turtle ki default animation (jo har move pe screen refresh karti hai) band kar deta hai — is se hum **khud control** karte hain ke kab screen update ho, jo smooth animation ke liye zaroori hai
- `screen.update()` — manually screen ko refresh karta hai
- `time.sleep(0.1)` — game ki speed control karta hai (chota number = fast game)
- Ye pattern (`tracer(0)` + manual `update()` + `sleep()`) **game loops** banane ka standard tareeqa hai

---

## 3️⃣ Building the Snake's Body (`snake.py`)

Snake body **3 segments** se shuru hoti hai (turtle objects ki list), aur jaise jaise khana khati hai, lambi hoti jati hai.

### Step 1: Starting Positions

```python
from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
```

**Explanation:** Har segment ke darmiyan 20 pixels ka fasla hai — ye `MOVE_DISTANCE` ke barabar hai, taake jab snake move kare to segments ekdum sahi tareeqe se ek dusre ki jagah aa sakein.

### Step 2: `Snake` Class

```python
class Snake:
    """Models the snake with multiple body segments that move together."""

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        """Creates the initial 3-segment snake body."""
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        """Adds a new square segment at the given position."""
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)
```

**Explanation:**
- `__init__` constructor `segments` (khali list) banata hai, phir `create_snake()` call kar ke isse fill karta hai
- `self.head = self.segments[0]` — pehla segment "head" ke tor pe reference kiya jata hai (movement/direction control ke liye important)
- `add_segment()` — ek naya turtle object banata hai (square shape), white color, aur specified position pe rakhta hai — ye method baad mein snake ko "grow" karne ke liye bhi reuse hoga

---

## 4️⃣ Moving the Snake (The Tricky Part!)

Naya programmer aksar galti karta hai: har segment ko independently move karne ki koshish karta hai. **Sahi tareeqa** hai — **peeche wale segments ko aage wale ki jagah bhejna**, aur sirf head ko naya move dena.

```python
def move(self):
    """Moves the snake forward by moving each segment to the position of the one in front of it."""
    for seg_num in range(len(self.segments) - 1, 0, -1):
        new_x = self.segments[seg_num - 1].xcor()
        new_y = self.segments[seg_num - 1].ycor()
        self.segments[seg_num].goto(new_x, new_y)
    self.head.forward(MOVE_DISTANCE)
```

**Explanation (Ye sabse important logic hai):**
- Loop **peeche se shuru hota hai** (`range(len(self.segments) - 1, 0, -1)`) — yani sabse aakhri segment se
- Har segment apni **agle wale (front wale) ki current position** pe chala jata hai (`segments[seg_num - 1]`)
- Sabse aakhir mein, sirf `self.head.forward()` call hota hai — head hi asal mein "move" karta hai, baaki sab sirf "follow" karte hain
- **Reverse order mein loop chalana zaroori hai** — agar hum front se start karte, to sare segments ek hi position pe overlap ho jate (kyunke front wala already move ho chuka hota)

**Visual Example:**
```
Before move:  Head(0,0) → Body1(-20,0) → Body2(-40,0)
Step 1: Body2 jata hai Body1 ki jagah  →  Body2(-20,0)
Step 2: Body1 jata hai Head ki jagah   →  Body1(0,0)
Step 3: Head khud forward move karta hai → Head(20,0)

After move:  Head(20,0) → Body1(0,0) → Body2(-20,0)
```

---

## 5️⃣ Direction Control Methods

```python
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


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

**Explanation (Reverse-Prevention Logic):**
- Turtle mein directions **degrees** mein hoti hain: Right = 0°, Up = 90°, Left = 180°, Down = 270°
- Har method **check karta hai ke snake abhi opposite direction mein to nahi ja raha** — e.g. `up()` sirf tab chalega jab snake pehle se `DOWN` na ja raha ho
- Ye check zaroori hai kyunke **real Snake game mein snake apni hi body se ulta nahi takra sakta** — agar ye check na ho, to snake "180° turn" kar ke khud se collide ho jayega

---

## 6️⃣ Full `snake.py`

```python
from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    """Models the snake with multiple body segments that move and turn together."""

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

## 7️⃣ Full `main.py`

```python
from turtle import Screen
from snake import Snake
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()

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

screen.exitonclick()
```

**Explanation:**
- `snake = Snake()` — poori snake ek object ke through control hoti hai
- `screen.onkey(fun=snake.up, key="Up")` — key press hone pe snake ka apna method (`snake.up`) call hota hai, kyunke Snake class encapsulation follow karti hai
- Main game loop mein `snake.move()` continuously call hota hai — is se snake automatically forward chalti rehti hai, chahe koi key press ho ya na ho (yehi asal Snake game ka behavior hai)

---

## 📸 Screenshot


<img width="996" height="717" alt="1" src="https://github.com/user-attachments/assets/a6f0e989-3eb5-4f43-8771-e16a0dd1c07d" />

---

## ✅ Key Takeaways
- `screen.tracer(0)` + manual `screen.update()` + `time.sleep()` — game loop banane ka standard pattern hai
- Snake body ek **list of Turtle objects** hai, jisme har object apni khud ki position rakhta hai
- Movement logic **reverse order** mein chalta hai — peeche wale segments aage walon ki jagah lete hain, sirf head asal mein move karta hai
- Direction control mein **reverse-prevention check** zaroori hai taake snake khud se collide na ho
- Poore game ko `Snake` class mein encapsulate karna (Day 16 wala concept) code ko clean aur `main.py` ko simple rakhta hai

---

## 🔗 Practice Task
- Snake ki starting length ko 3 se badha kar 5 kar do
- Snake ki speed (game loop ka `time.sleep()` value) change kar ke dekho farq
- WASD keys ko bhi arrow keys ke sath bind karo taake dono se control ho sake

---

**Note:** Part 2 mein hum food/snack add karenge (jisse snake grow ho), score tracking, aur collision detection (wall aur khud se takrana) implement karenge.
