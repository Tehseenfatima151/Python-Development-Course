# Day 22 – Pong Game Basics (Part 1: Paddles & Ball Movement)

## 📌 Overview
Is session mein humne classic **Pong Game** banana shuru kiya. Part 1 mein humne wo **basic building blocks** seekhe jo Pong banane ke liye zaroori hain — `Paddle` aur `Ball` classes (Turtle se inherit), `screen.update()` wala game loop, keyboard se paddles move karna, aur ball ki basic movement/wall-bounce logic. Ye Snake Game (Day 20-21) wale concepts ka hi extension hai, bas is dafa **do players** aur **physics-jaisi bouncing** involved hai.

---

## 1️⃣ Project Structure

```
pong_game_part1/
├── main.py
├── paddle.py
└── ball.py
```

| File | Responsibility |
|------|-----------------|
| `paddle.py` | `Paddle` class — rectangle shape, up/down movement |
| `ball.py` | `Ball` class — movement, wall-bounce logic |
| `main.py` | Screen setup, event listeners, game loop |

---

## 2️⃣ Screen Setup (`main.py` — Base)

```python
from turtle import Screen
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.05)

screen.exitonclick()
```

**Explanation:** Bilkul Snake Game jaisa pattern — `tracer(0)` + manual `update()` + `time.sleep()`. Yahan `sleep` ki value chhoti (0.05) rakhi hai taake ball smooth aur fast move kare, jaisa real Pong mein hota hai.

---

## 3️⃣ Building the `Paddle` Class

Pong mein **2 paddles** hoti hain (left player, right player) — dono same behavior rakhte hain, is liye ek hi class dono ke liye reuse hoti hai.

```python
from turtle import Turtle

class Paddle(Turtle):
    """Models a paddle that can move up and down."""

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)   # Lamba, patla rectangle banata hai
        self.penup()
        self.goto(position)

    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)
```

**Explanation:**
- `class Paddle(Turtle):` — Inheritance (Day 21 wala concept) — Paddle, Turtle ki saari properties leta hai
- `shapesize(stretch_wid=5, stretch_len=1)` — normal square ko **lamba aur patla** bana deta hai, taake paddle jaisa dikhe
- `go_up()`/`go_down()` — sirf `y` coordinate change karte hain, `x` same rehta hai (paddle sirf upar-neeche move karta hai)

### Creating Two Paddles

```python
right_paddle = Paddle((350, 0))
left_paddle = Paddle((-350, 0))
```

Same class se **do independent objects** ban rahe hain — har paddle apni khud ki position rakhta hai (Day 19 wala "multiple instances" concept yaad karo).

---

## 4️⃣ Building the `Ball` Class

```python
from turtle import Turtle

class Ball(Turtle):
    """Models the ball that moves around and bounces off walls."""

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
        """Reverses vertical direction (used when ball hits top/bottom wall)."""
        self.y_move *= -1
```

**Explanation:**
- `x_move` aur `y_move` — ball ki current speed/direction store karte hain (ye **state** hai, Day 19 wala concept)
- `move()` — har frame mein ball ko current direction mein aage badhata hai
- `bounce_y()` — `y_move` ko negative kar deta hai (`* -1`), is se direction **reverse** ho jati hai — agar upar ja raha tha, ab neeche jayega

---

## 5️⃣ Wall Bounce Logic (`main.py` Mein)

```python
ball = Ball()

while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Top/bottom wall bounce
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
```

**Explanation:** Agar ball ki `y` position screen ki upar/neeche boundary (280) cross kar jaye, to `bounce_y()` call ho kar direction reverse kar deta hai — ball wapis andar bounce karti hai.

---

## 6️⃣ Keyboard Controls for Both Paddles

```python
screen.listen()
screen.onkeypress(right_paddle.go_up, "Up")
screen.onkeypress(right_paddle.go_down, "Down")
screen.onkeypress(left_paddle.go_up, "w")
screen.onkeypress(left_paddle.go_down, "s")
```

**Explanation:** Right paddle **arrow keys** se control hota hai, left paddle **W/S keys** se — is se do players ek hi keyboard pe simultaneously khel sakte hain.

---

## 7️⃣ Full Combined `main.py` (Part 1)

```python
from turtle import Screen
from paddle import Paddle
from ball import Ball
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

right_paddle = Paddle((350, 0))
left_paddle = Paddle((-350, 0))
ball = Ball()

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

    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

screen.exitonclick()
```

---

## 📸 Screenshot

<img width="1365" height="725" alt="1" src="https://github.com/user-attachments/assets/2cfa4330-982e-4043-a44d-1b018840710c" />

---

## ✅ Key Takeaways
- Pong ka structure Snake Game se milta julta hai — inheritance (`Paddle(Turtle)`, `Ball(Turtle)`) aur game-loop pattern reuse hote hain
- Ek hi class (`Paddle`) se **multiple independent objects** banana efficient hai jab behavior same ho
- Ball ki state (`x_move`, `y_move`) track karna zaroori hai taake movement aur bouncing consistent rahe
- `bounce_y()` jaisa simple direction-reversal logic (`* -1`) physics jaisa effect create karta hai bina complex math ke
- Do players ek sath alag-alag keys (Arrow keys vs W/S) se control kar sakte hain — `onkeypress()` multiple bindings support karta hai

---

**Note:** Ye Part 1 hai — paddles move karte hain aur ball wall se bounce karti hai, lekin abhi **paddle collision aur scoring** missing hai. Wo agle project (Complete Pong Game) mein cover hoga.
