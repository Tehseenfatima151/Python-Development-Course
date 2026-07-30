# Day 18 – Turtle Graphics, Tuples, Importing Modules & Hirst Painting

## 📌 Overview
Is session mein humne **Turtle graphics** ka concept seekha — Python mein drawing/graphics kaise banate hain, **tuples** kya hote hain (aur lists se kaise different hain), aur **modules import** karne ka detailed tareeqa. Iske baad humne ye sab concepts use kar ke Damien Hirst ke famous "spot painting" ko replicate kiya — random colored dots ki grid banai.

---

## 1️⃣ Importing Modules (Detail)

**Module** ek `.py` file hoti hai jisme reusable code (functions, classes) hota hai. Python mein bohot saare **built-in modules** already available hain jo hum `import` kar ke use kar sakte hain — bina khud se likhe.

### Different Ways to Import

```python
import turtle                    # Poora module import karna
```

```python
from turtle import Turtle, Screen   # Sirf specific cheezein import karna
```

```python
import turtle as t               # Alias (chota naam) dena
```

**Explanation:**
- `import turtle` — poora module import hota hai, use karne ke liye `turtle.function_name()` likhna parta hai
- `from turtle import Turtle` — sirf `Turtle` class import hoti hai, seedha `Turtle()` likh sakte hain, `turtle.` likhne ki zaroorat nahi
- `import turtle as t` — module ka naam chota (alias) rakh dete hain, jaise `t.something()`

### Third-Party Modules

Kuch modules Python ke sath built-in nahi aate, unhe pehle **install** karna parta hai:

```bash
pip install package_name
```

Phir usse import kar ke use karte hain, jaise `pandas`, `requests`, etc.

---

## 2️⃣ What is Turtle Graphics?

**Turtle** Python ka ek built-in module hai jo screen pe drawing banane ke liye use hota hai. Isme ek "turtle" (cursor) hota hai jo screen pe ghoomta hai aur jahan se guzarta hai wahan line kheenchta jata hai — bilkul jaise koi pen kagaz pe chalti hai.

```python
from turtle import Turtle, Screen

screen = Screen()          # Ek naya drawing window banata hai
timmy = Turtle()           # Ek naya turtle (cursor) banata hai

timmy.forward(100)         # 100 pixels aage move karta hai (line kheenchte hue)

screen.exitonclick()       # Window ko click hone tak khula rakhta hai
```

---

## 3️⃣ Basic Turtle Commands

### Movement

```python
timmy.forward(100)     # Aage move karna
timmy.backward(50)     # Peeche move karna
timmy.right(90)        # Right taraf ghumna (degrees mein)
timmy.left(90)         # Left taraf ghumna
```

### Pen Control

```python
timmy.penup()           # Pen utha lena (line nahi banegi jab move ho)
timmy.pendown()         # Pen wapis neeche karna (line banegi)
timmy.pensize(5)        # Line ki thickness set karna
timmy.pencolor("red")   # Line ka color set karna
```

### Speed & Shape

```python
timmy.speed(10)         # Turtle ki speed set karna (1 = slow, 10 = fast, 0 = instant)
timmy.shape("turtle")   # Cursor ka shape set karna
```

### Drawing Basic Shapes

```python
# Square banane ke liye
for _ in range(4):
    timmy.forward(100)
    timmy.right(90)
```

```python
# Kisi bhi polygon (bahu-bhuji shape) banane ke liye
def draw_shape(num_sides):
    angle = 360 / num_sides
    for _ in range(num_sides):
        timmy.forward(100)
        timmy.right(angle)

draw_shape(6)   # Hexagon (6 sides)
```

**Explanation:** Kisi bhi polygon ka bahar wala angle `360 / number_of_sides` hota hai — is formula se hum koi bhi shape draw kar sakte hain.

---

## 4️⃣ What is a Tuple?

**Tuple** list jaisa hi ek data type hai, lekin ek bara farq ke sath: tuple **immutable** hota hai — yani ek baar banne ke baad usme koi change (add/remove/modify) nahi kiya ja sakta.

```python
my_tuple = (1, 2, 3)
print(my_tuple[0])   # Output: 1 (indexing list jaisi hi hoti hai)
```

### List vs Tuple

| List | Tuple |
|------|-------|
| `[1, 2, 3]` — square brackets | `(1, 2, 3)` — round brackets |
| Mutable — change ho sakti hai | Immutable — change nahi ho sakta |
| `append()`, `remove()` waghera available | Koi modification method available nahi |
| Slower (kyunke changeable hai) | Faster (kyunke fixed hai) |

```python
my_tuple = (1, 2, 3)
my_tuple[0] = 100   # TypeError: 'tuple' object does not support item assignment
```

### Tuples Kab Use Karte Hain?

Jab hum chahte hain ke data **accidentally change na ho** — jaise coordinates, colors (RGB values), ya koi bhi fixed set of values.

```python
color = (255, 0, 0)   # RGB tuple — red color
coordinates = (10, 20)  # x, y position — fixed rehni chahiye
```

Turtle graphics mein colors ko aksar **RGB tuple** ki soorat mein use karte hain:

```python
screen.colormode(255)              # RGB values 0-255 range mein use karne ke liye
random_color = (23, 145, 200)       # Ek RGB tuple
timmy.pencolor(random_color)
```

---

## 5️⃣ Building the Hirst Painting

**Concept:** Damien Hirst ek famous artist hai jo "spot paintings" banate hain — ek grid mein bohot saare colorful dots. Humne isse Python code se replicate kiya, `random` module se random colors choose kar ke.

### Step 1: Setup

```python
from turtle import Turtle, Screen
import random

tim = Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

screen = Screen()
screen.colormode(255)
```

**Explanation:**
- `speed("fastest")` — turtle ko sabse fast speed pe set karta hai (grid bara hai, fast hona zaroori hai)
- `penup()` — dots ke darmiyan lines nahi chahiye, sirf dots
- `hideturtle()` — cursor arrow ko hide kar deta hai, sirf dots dikhengi
- `colormode(255)` — RGB colors 0-255 range mein use karne ke liye enable karta hai

### Step 2: Color Palette Banana (List of Tuples)

Real Hirst painting ke colors ko manually extract kar ke ek list of RGB tuples banate hain:

```python
color_list = [
    (247, 216, 55), (242, 226, 12), (242, 202, 12), (240, 65, 35),
    (237, 28, 36), (196, 40, 27), (26, 90, 44), (10, 136, 61),
    (69, 176, 78), (13, 152, 186), (27, 91, 156), (33, 63, 145),
    (240, 65, 35), (69, 176, 78), (247, 216, 55), (26, 90, 44),
    (18, 82, 154), (196, 40, 27), (242, 226, 12), (10, 136, 61),
]
```

**Explanation:** Ye ek "list of tuples" hai — har tuple ek RGB color represent karta hai. Tuples yahan zaroori hain kyunke colors ki values fixed rehni chahiye, galti se change na ho.

### Step 3: Positioning Logic

```python
tim.setheading(225)   # 225 degree angle pe move karo (bottom-left)
tim.forward(300)      # Grid ke starting point pe pohanchne ke liye
tim.setheading(0)     # Wapis right taraf face karo
```

### Step 4: Drawing the Grid of Dots

```python
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)     # Upar move karo
        tim.forward(50)
        tim.setheading(180)     # Wapis left face karo
        tim.forward(500)        # Line ke shuru mein wapis jao
        tim.setheading(0)       # Phir se right face karo
```

**Explanation:**
- `tim.dot(20, random.choice(color_list))` — ek dot banata hai, size 20, random color list mein se choose kar ke
- Har 10 dots ke baad (`dot_count % 10 == 0`), turtle upar wali row pe chala jata hai aur wapis left se start karta hai — is se **grid pattern** banta hai
- `random.choice(color_list)` — har baar list mein se ek random tuple (color) select karta hai

---

## 6️⃣ Full Combined Program

```python
from turtle import Turtle, Screen
import random

tim = Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

screen = Screen()
screen.colormode(255)

color_list = [
    (247, 216, 55), (242, 226, 12), (242, 202, 12), (240, 65, 35),
    (237, 28, 36), (196, 40, 27), (26, 90, 44), (10, 136, 61),
    (69, 176, 78), (13, 152, 186), (27, 91, 156), (33, 63, 145),
    (240, 65, 35), (69, 176, 78), (247, 216, 55), (26, 90, 44),
    (18, 82, 154), (196, 40, 27), (242, 226, 12), (10, 136, 61),
]

tim.setheading(225)
tim.forward(300)
tim.setheading(0)

number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)

screen.exitonclick()
```

---

## 7️⃣ Bonus: Random Walk Drawing (Extra Turtle Practice)

```python
from turtle import Turtle, Screen
import random

tim = Turtle()
screen = Screen()
screen.colormode(255)

directions = [0, 90, 180, 270]

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

tim.speed("fastest")
tim.pensize(3)

for _ in range(200):
    tim.pencolor(random_color())
    tim.forward(30)
    tim.setheading(random.choice(directions))

screen.exitonclick()
```

---

## 📸 Screenshot


<img width="1202" height="722" alt="2" src="https://github.com/user-attachments/assets/73784ce4-44d3-4912-82c1-ff169573fc50" />


<img width="1204" height="726" alt="1" src="https://github.com/user-attachments/assets/1dfa6448-2910-47e3-a06d-2f63552e9985" />

---

## ✅ Key Takeaways
- Modules ko `import` karne ke 3 tareeqe hain: poora module, specific parts, ya alias ke sath
- Turtle module screen pe drawing banane ke liye use hota hai — movement, pen control, aur speed commands se
- Tuples lists jaisi hoti hain lekin **immutable** — ek baar ban jayein to change nahi ho sakti
- Tuples fixed data (jaise RGB colors, coordinates) store karne ke liye best hain
- `random.choice()` ek list (ya list of tuples) mein se random item select karta hai
- Grid patterns banane ke liye positioning logic (`setheading()`, `forward()`) aur modulus operator (`%`) ka combination use hota hai
- Real-world art ko code se replicate karna geometry, loops, aur randomization ka acha combined practice hai

---

## 🔗 Practice Task
- Dots ki number aur spacing change kar ke apni khud ki grid size banao (jaise 15x15)
- `random_color()` function use kar ke poori tarah random colors wali painting banao (fixed palette ke bagair)
- Turtle se apna khud ka naam ya koi simple shape (star, flower) draw karo loops use kar ke
