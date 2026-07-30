# Day 19 – Turtle Event Listeners, State & Multiple Turtle Instances

## 📌 Overview
Is session mein humne Turtle graphics ko **interactive** banana seekha — **event listeners** (keyboard aur mouse ke through turtle ko control karna), **state management** (score, position, direction track karna), aur **multiple turtle instances** ek sath use karna. In concepts ko practically apply kar ke humne 2 mini-projects banaye: **Etch-a-Sketch** aur **Turtle Race**.

---

## 1️⃣ Event Listeners

**Event Listener** ek function hai jo kisi specific "event" (jaise key press, mouse click) hone ka intezar karta hai, aur jaise hi wo event hota hai, ek specified function ko **automatically call** kar deta hai.

Ye pichle sessions se different hai — pehle hum `input()` se user ka wait karte thay (program rukta tha), lekin event listeners ke sath program chalta rehta hai aur **background mein sun raha hota hai** ke koi key dabi ya nahi.

### Keyboard Event Listener

```python
from turtle import Turtle, Screen

timmy = Turtle()
screen = Screen()

def move_forward():
    timmy.forward(10)

screen.listen()                              # Screen ko keyboard input sunne ke liye ready karta hai
screen.onkey(key="space", fun=move_forward)   # Jab "space" key dabein, move_forward() call ho

screen.exitonclick()
```

**Explanation:**
- `screen.listen()` — screen ko "active listening mode" mein daal deta hai
- `screen.onkey(key="...", fun=...)` — batata hai ke konsi key dabne pe konsa function chalna hai
- `fun=move_forward` — **function ka naam** diya hai (bina `()` ke), kyunke hum function ko call nahi kar rahe, sirf reference de rahe hain ke "jab event ho to ise chalana"

### Multiple Key Bindings

```python
def move_up():
    timmy.setheading(90)
    timmy.forward(10)

def move_down():
    timmy.setheading(270)
    timmy.forward(10)

def move_left():
    timmy.setheading(180)
    timmy.forward(10)

def move_right():
    timmy.setheading(0)
    timmy.forward(10)

screen.listen()
screen.onkey(key="Up", fun=move_up)
screen.onkey(key="Down", fun=move_down)
screen.onkey(key="Left", fun=move_left)
screen.onkey(key="Right", fun=move_right)
```

**Explanation:** Har arrow key ke liye alag function bana kar bind karte hain — jaise hi koi key dabti hai, uska corresponding function chal jata hai.

### Mouse Click Event Listener

```python
def clicked_screen(x, y):
    print(f"Clicked at position: {x}, {y}")

screen.onscreenclick(clicked_screen)
```

**Explanation:** Click hone pe function ko automatically `x` aur `y` coordinates mil jate hain jahan click hui thi.

---

## 2️⃣ State (Program Ki Current Situation Track Karna)

**State** ka matlab hai program ke current "hone ki situation" ko track karna — jaise score kitna hai, turtle kaha khara hai, ya game kis stage pe hai. State ko humesha variables mein store karte hain jo events ke hone se update hoti hain.

```python
from turtle import Turtle, Screen

timmy = Turtle()
screen = Screen()

score = 0   # Ye state hai

def increase_score():
    global score
    score += 1
    print(f"Score: {score}")

screen.listen()
screen.onkey(key="space", fun=increase_score)

screen.exitonclick()
```

**Explanation:**
- `score` variable **state** hai — ye track karta hai ke abhi kya situation hai
- Har baar jab space dabti hai, state update hoti hai (`score += 1`)
- `global` keyword yahan zaroori hai kyunke `score` function ke bahar define hai aur function ke andar se update karna hai (Day 12 wala concept yaad karo)

---

## 3️⃣ Multiple Turtle Instances

Jaisa Day 17 mein humne multiple objects (classes se) banaye thay, waise hi hum **multiple Turtle objects** bhi bana sakte hain — har turtle apni khud ki position, color, aur state independently rakhta hai.

```python
from turtle import Turtle, Screen

screen = Screen()

turtle_1 = Turtle()
turtle_1.color("red")
turtle_1.penup()
turtle_1.goto(-100, 0)

turtle_2 = Turtle()
turtle_2.color("blue")
turtle_2.penup()
turtle_2.goto(0, 0)

turtle_3 = Turtle()
turtle_3.color("green")
turtle_3.penup()
turtle_3.goto(100, 0)

screen.exitonclick()
```

**Explanation:** Har `Turtle()` call se ek naya independent turtle object banta hai — `turtle_1` ka color change karne se `turtle_2` pe koi asar nahi parta, kyunke har object apni alag attributes rakhta hai (encapsulation, Day 16 wala concept).

### Creating Multiple Turtles Dynamically (Loop se)

```python
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
all_turtles = []

for turtle_color in colors:
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(turtle_color)
    all_turtles.append(new_turtle)
```

**Explanation:** List of colors pe loop chala kar har color ke liye ek naya turtle object banaya aur `all_turtles` list mein store kar diya — is se hum kitne bhi turtles dynamically bana sakte hain.

---

## 4️⃣ Project 1: Etch-a-Sketch

**Concept:** Ek classic toy jisme arrow keys se drawing control karte hain, aur "c" key dabane se screen clear ho jati hai.

```python
from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()


def move_forward():
    tim.forward(10)


def turn_left():
    new_heading = tim.heading() + 10
    tim.setheading(new_heading)


def turn_right():
    new_heading = tim.heading() - 10
    tim.setheading(new_heading)


def clear_screen():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


screen.listen()
screen.onkey(fun=move_forward, key="Up")
screen.onkey(fun=turn_left, key="Left")
screen.onkey(fun=turn_right, key="Right")
screen.onkey(fun=clear_screen, key="c")

screen.exitonclick()
```

**Explanation:**
- `tim.heading()` — current direction (degrees mein) return karta hai — ye bhi ek **state** hai
- `turn_left()`/`turn_right()` — current heading mein 10 degrees add/subtract kar ke naya angle set karte hain, isse smooth turning hoti hai
- `clear_screen()` — screen clear karta hai aur turtle ko wapis center (`home()`) bhej deta hai

---

## 5️⃣ Project 2: Turtle Race

**Concept:** User ek color guess karta hai, phir multiple turtles randomly race karte hain — jo bhi pehle finish line cross kare wahi winner hai, aur user ka guess check hota hai.

```python
from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

user_guess = screen.textinput(title="Make your guess", prompt="Which turtle will win the race? Enter a color: ")

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
all_turtles = []

y_position = -70
for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_position)
    y_position += 30
    all_turtles.append(new_turtle)

if user_guess:
    is_race_on = True

while is_race_on:
    for racing_turtle in all_turtles:
        if racing_turtle.xcor() > 230:      # Finish line check
            is_race_on = False
            winning_color = racing_turtle.pencolor()

            if winning_color == user_guess:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")

        random_distance = random.randint(0, 10)
        racing_turtle.forward(random_distance)

screen.exitonclick()
```

**Explanation:**
- `screen.textinput()` — ek popup dialog box khol kar user se text input leta hai
- Loop se **6 turtles dynamically** banaye gaye, har ek apni row mein positioned
- `racing_turtle.xcor()` — turtle ki current x-coordinate (position) return karta hai — ye bhi **state tracking** hai
- Jab koi turtle finish line (`x > 230`) cross kare, race ruk jati hai aur winner ka color user ke guess se compare hota hai
- Har turtle har loop cycle mein random distance (0-10) forward move karta hai — is se race unpredictable rehti hai

---

## 📸 Screenshot

<!-- Turtle window ka screenshot yahan drag & drop karo -->
<img width="700" height="705" alt="1" src="https://github.com/user-attachments/assets/63f895d0-a1cf-4af7-8f56-f523d048041f" />

---

## ✅ Key Takeaways
- Event listeners program ko **interactive** banate hain — `input()` ki tarah rukte nahi, background mein events sunte rehte hain
- `screen.listen()` + `screen.onkey()` keyboard input handle karte hain, `screen.onscreenclick()` mouse clicks
- State variables (jaise `score`, `heading`, `xcor()`) program ki current situation track karte hain aur events ke through update hote hain
- Multiple Turtle objects independently apni state rakhte hain — ek ko change karne se doosre pe asar nahi parta
- Loop se dynamically multiple turtles banana scalable aur reusable approach hai
- Etch-a-Sketch event-driven drawing dikhata hai, Turtle Race multiple instances + randomization + state comparison dikhata hai

---

## 🔗 Practice Task
- Etch-a-Sketch mein ek naya key bind karo jo pen color randomly change kare
- Turtle Race mein turtles ki number user se input karwao (fixed 6 ki bajaye)
- Ek naya event listener banao jo mouse click pe turtle ko us position pe teleport kar de (`goto(x, y)` use kar ke)
