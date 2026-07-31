# Project 2 – Complete Pong Game

## 📌 Overview
Ye Day 22 (Part 1) ka **complete/finished version** hai — usi Pong Game mein ab **paddle collision detection**, **miss/scoring logic**, aur **live scoreboard** add ki gayi hai. Poora game ab professionally 4 files mein organized hai — `Paddle`, `Ball`, `Scoreboard` classes (sab Turtle se inherit) + `main.py` jo sabko coordinate karta hai.

---

## 1️⃣ Project Structure

```
pong_complete/
├── main.py
├── paddle.py
├── ball.py
└── scoreboard.py
```

| File | Responsibility |
|------|-----------------|
| `paddle.py` | `Paddle` class — movement (Part 1 se same) |
| `ball.py` | `Ball` class — movement, wall bounce, paddle bounce, reset |
| `scoreboard.py` | `Scoreboard` class — dono players ka score track aur display karta hai |
| `main.py` | Poora game loop — collision checks, scoring, coordination |

---

## 2️⃣ What's New Compared to Part 1?

| Part 1 (Day 22) | Project 2 (Complete) |
|-------------------|------------------------|
| Ball sirf top/bottom walls se bounce karti thi | Ball ab **paddles se bhi bounce** karti hai |
| Koi scoring nahi thi | **Live scoreboard** — dono players ka score track hota hai |
| Ball miss hone pe kuch nahi hota tha | Ball miss hone pe **point milta hai** aur ball **reset** hoti hai |
| Sirf 2 files (`paddle.py`, `ball.py`) | 3 classes — `Scoreboard` bhi add hui |

---

## 3️⃣ `Ball` Class — Extended with Paddle Bounce & Reset

```python
from turtle import Turtle


class Ball(Turtle):
    """Models the ball: movement, wall bounce, paddle bounce, and resetting."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Reverses vertical direction — used for top/bottom wall collisions."""
        self.y_move *= -1

    def bounce_x(self):
        """Reverses horizontal direction and slightly speeds up — used for paddle collisions."""
        self.x_move *= -1
        self.move_speed *= 0.9   # Har paddle-hit ke baad game thora tez hota hai

    def reset_position(self):
        """Sends the ball back to the center and reverses its x direction (serves to the other side)."""
        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_x()
```

**Explanation:**
- `bounce_x()` — paddle se takrane pe horizontal direction reverse hoti hai, saath hi speed thori barh jati hai (`* 0.9` — number chota, delay kam, matlab speed zyada) — is se game progressively challenging hota jata hai
- `reset_position()` — jab koi player point kare, ball wapis center mein aati hai aur naye direction mein serve hoti hai

---

## 4️⃣ `Scoreboard` Class

```python
from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    """Models the scoreboard, tracking and displaying both players' scores."""

    def __init__(self):
        super().__init__()
        self.l_score = 0
        self.r_score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears and redraws both scores."""
        self.clear()
        self.goto(-100, 200)
        self.write(self.l_score, align="center", font=FONT)
        self.goto(100, 200)
        self.write(self.r_score, align="center", font=FONT)

    def l_point(self):
        """Increments the left player's score."""
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        """Increments the right player's score."""
        self.r_score += 1
        self.update_scoreboard()
```

**Explanation:** Dono players ke scores alag variables (`l_score`, `r_score`) mein track hote hain — jaise hi koi point score kare, corresponding method call ho kar score barhata hai aur screen refresh kar deta hai.

---

## 5️⃣ Paddle Collision Detection

```python
# Right paddle collision
if ball.distance(right_paddle) < 50 and ball.xcor() > 320:
    ball.bounce_x()

# Left paddle collision
if ball.distance(left_paddle) < 50 and ball.xcor() < -320:
    ball.bounce_x()
```

**Explanation:**
- `ball.distance(paddle)` — Day 21 wala concept, do turtles ke darmiyan fasla nikalta hai
- `< 50` — agar ball paddle ke bohot qareeb ho
- `ball.xcor() > 320` — **extra check zaroori hai**, warna ball paddle ke aage se guzarte hue bhi galti se "collision" detect kar sakti hai (sirf distance check kaafi nahi, x-position bhi confirm karni parti hai ke ball waqai paddle ki edge pe hai)

---

## 6️⃣ Miss Detection (Scoring Logic)

```python
# Ball right wall cross kar gayi -> left player scores
if ball.xcor() > 380:
    ball.reset_position()
    scoreboard.l_point()

# Ball left wall cross kar gayi -> right player scores
if ball.xcor() < -380:
    ball.reset_position()
    scoreboard.r_point()
```

**Explanation:** Agar ball paddle ko miss kar ke seedha screen ki side-wall tak pohanch jaye, to matlab wo player miss kar gaya — **doosre player ko point milta hai**, aur ball reset ho jati hai.

---

## 7️⃣ Full Combined `main.py`

```python
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

right_paddle = Paddle((350, 0))
left_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(right_paddle.go_up, "Up")
screen.onkeypress(right_paddle.go_down, "Down")
screen.onkeypress(left_paddle.go_up, "w")
screen.onkeypress(left_paddle.go_down, "s")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Top/bottom wall bounce
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Right paddle collision
    if ball.distance(right_paddle) < 50 and ball.xcor() > 320:
        ball.bounce_x()

    # Left paddle collision
    if ball.distance(left_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # Right side miss -> left player scores
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # Left side miss -> right player scores
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()
```

---

## 📸 Screenshot

<img width="1365" height="725" alt="1" src="https://github.com/user-attachments/assets/5e0df9d3-164c-49e1-b6b3-1e81e6ce66bc" />

---

## ✅ Key Takeaways
- Existing classes (`Paddle`, `Ball`) **extend** karna (naye methods add karna) code reuse ka best example hai — Part 1 ka base structure change nahi karna para
- Paddle collision ke liye sirf `distance()` kaafi nahi — `xcor()` ka extra check zaroori hai taake false-positive collisions na ho
- Progressive difficulty (`move_speed *= 0.9` har hit pe) simple math se game ko interesting banata hai
- Miss detection ka logic seedha hai: agar ball kisi bhi extreme wall tak pohanch jaye bina paddle se takraye, to opposite player ko point milta hai
- Poora Pong Game ab **3 classes + main.py** mein professionally organized hai, bilkul Snake Game jaisi structure follow karte hue

---

## 🔗 Practice Task
- Ek "winning score" add karo (jaise 5 points) jispe pohanchte hi "Player X Wins!" show ho aur game ruk jaye
- Paddle ki speed configurable banao (difficulty levels ke liye)
- Center mein ek dashed line add karo (turtle se) jaisa asal Pong table mein hota hai
