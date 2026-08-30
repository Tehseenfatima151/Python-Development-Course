# Day 95 — Game Development Portfolio Project: Snake Game

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Classic Snake Game

A fully playable **Snake game** built with Python's `turtle` module — arrow-key controls, growing snake body, random food spawning, wall/self collision detection, and a **persisted high score** that survives between play sessions. Built with clean OOP structure (separate `Snake`, `Food`, and `Scoreboard` classes) rather than one big script.

The game logic was actually executed on a virtual display before writing this README — real output below, not just a plan (see "Tested Output").

---

## 🧠 Concepts Covered

### 1. Object-Oriented structure — one class per responsibility
Instead of one large file, the game is split into 4 files, each with a single job:
```
snake.py       -> Snake class: body, movement, growth, direction
food.py        -> Food class: random spawning
scoreboard.py  -> Scoreboard class: score display + high score persistence
main.py        -> ties everything together into the game loop
```
This mirrors real-world project structure — each class can be understood, tested, and modified independently.

### 2. The "shuffle segments forward" movement trick
```python
def move(self):
    for seg_num in range(len(self.segments) - 1, 0, -1):
        new_x = self.segments[seg_num - 1].xcor()
        new_y = self.segments[seg_num - 1].ycor()
        self.segments[seg_num].goto(new_x, new_y)
    self.head.forward(MOVE_DISTANCE)
```
Rather than tracking a separate "direction" for every segment, each segment simply jumps to where the segment *in front of it* just was — looping **backwards** through the list so segments don't all overwrite each other before they've each moved. Only the head actually "moves" forward in the traditional sense.

### 3. Preventing 180° reversal (a classic Snake bug)
```python
def up(self):
    if self.head.heading() != DOWN:
        self.head.setheading(UP)
```
Without this check, pressing the opposite arrow key while moving would make the snake instantly collide with its own second segment — checking the current heading before allowing the change prevents that.

### 4. Extending the snake without recalculating positions
```python
def extend(self):
    self.add_segment(self.segments[-1].position())
```
The new segment starts exactly where the current last segment is — visually it looks stationary for one frame, then "catches up" naturally on the very next `move()` call, since movement is relative to the segment ahead of it.

### 5. Turtle's manual screen updates for smooth animation
```python
screen.tracer(0)   # disable automatic redraw
...
while game_is_on:
    screen.update()   # manually redraw only when we choose to
    time.sleep(0.1)
```
By default, turtle redraws after every single drawing command, which looks flickery/slow for a game loop. Turning off `tracer` and calling `update()` once per frame gives smooth, controlled animation.

### 6. Collision detection with distance checks
```python
if snake.head.distance(food) < 15:      # ate food
if snake.head.xcor() > 280 or ...:       # hit wall
if snake.head.distance(segment) < 10:    # hit own tail
```
Turtle objects have a built-in `.distance()` method — no manual coordinate-geometry formula needed to check if two shapes are close enough to count as a collision.

### 7. Persisting the high score across sessions
```python
def load_high_score(self):
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(self):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(self.high_score))
```
The high score is written to a plain text file only when it's actually beaten — so it survives closing and reopening the game, the same pattern used by `passwords.json` in the Day 85 project.

---

## 📂 Project Structure
```
day87/
├── main.py          # game loop, window setup, keyboard bindings
├── snake.py          # Snake class
├── food.py            # Food class
├── scoreboard.py       # Scoreboard class + high score file I/O
└── high_score.txt        # auto-created on first game over (not included)
```

## ▶️ How to Run
```bash
python main.py
```
Tkinter/Turtle ship with standard Python installs on Windows/Mac. On some Linux distributions: `sudo apt install python3-tk`.

**Controls:** Arrow keys to steer. Game ends on hitting a wall or the snake's own tail.

---

## 🧪 Tested Output
The game was run headlessly on a virtual display (Xvfb) before writing this README, simulating several real gameplay frames:

```
Initial snake segments: 3
Initial score: 0
Step 2: ate food!
Final snake segments: 4
Final score: 1
✅ Saved game_canvas.eps
```
The canvas was also exported to confirm real rendering occurred — the export contained a valid bounding box and 11 distinct drawn shapes/text elements (the 4 snake segments, the food dot, and the score text), confirming the window actually rendered the game correctly rather than just running the logic blind.

---
## 📸 Screenshot
<img width="1031" height="726" alt="1" src="https://github.com/user-attachments/assets/0fa0906c-ec22-43ef-8a32-9e70bba9a5e6" />

---
## ✅ Key Takeaways
- Splitting a game into `Snake` / `Food` / `Scoreboard` classes (instead of one script) makes each piece independently understandable and testable — the same principle as separating logic from GUI in the Day 85 Password Manager.
- The "shift each segment to the position of the one ahead of it" technique is the standard, elegant way to animate a growing snake body without manually tracking per-segment direction.
- `screen.tracer(0)` + manual `screen.update()` is essential for smooth animation in any turtle-based game loop — without it, games look flickery and slow.
- Turtle's built-in `.distance()` method handles collision detection without writing manual geometry formulas.
- Persisting a high score to a plain text file is a simple, effective pattern — same idea as JSON persistence, just for a single value.

## 📝 Practice Tasks
1. Add increasing speed as the score goes up (`time.sleep()` value shrinks every few points).
2. Add a "Play Again" prompt after game over instead of requiring the script to be re-run.
3. Add different colored food that's worth bonus points, spawning occasionally.
4. Package this into an `.exe`/`.app` using `pyinstaller` so it can be shared as a standalone download — a nice addition for a portfolio demo link.



