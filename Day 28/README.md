# Day 28 – Pomodoro App (Tkinter GUI)

## 📌 Overview

Day 28 mein humne Python ki **Tkinter GUI library** use karke ek **Pomodoro Timer Application** banai. Is project ka objective tha GUI development, countdown timer, event handling aur state management ko practically implement karna.

Pomodoro Technique ek productivity method hai jisme user kuch der focused work karta hai, phir short break leta hai. 4 work sessions complete hone ke baad ek long break milti hai.

Is project mein humne **Tkinter Widgets, Canvas, Images, `after()` function, Countdown Timer aur Session Tracking** ka use kiya.

---

# 🍅 What is the Pomodoro Technique?

Pomodoro cycle kuch is tarah work karti hai:

```text
Work
 ↓
Short Break
 ↓
Work
 ↓
Short Break
 ↓
Work
 ↓
Short Break
 ↓
Work
 ↓
Long Break
 ↓
Repeat
```

Testing ke liye timer values:

```python
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
```

Normally Pomodoro Technique:

* Work → 25 Minutes
* Short Break → 5 Minutes
* Long Break → 20 Minutes

---

# ✨ Features

* 🍅 Beautiful Tkinter GUI
* ⏱️ Live Countdown Timer
* ▶️ Start Button
* 🔄 Reset Button
* ✅ Automatic Session Tracking
* ✔ Work Completion Check Marks
* 🎨 Tomato Image using Canvas
* 🔁 Automatic Work & Break Switching

---

# 📁 Project Structure

```text
pomodoro/
│
├── main.py
└── tomato.png
```

| File         | Description              |
| ------------ | ------------------------ |
| `main.py`    | Main application logic   |
| `tomato.png` | Tomato image used in GUI |

---

# 🖥️ User Interface

The application contains:

* Title Label
* Canvas
* Tomato Image
* Countdown Timer
* Start Button
* Reset Button
* Check Marks Label

Simple and clean GUI design using **Tkinter Grid Layout**.

---

# 🎨 Constants

```python
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
```

Different colors are defined as constants to make the interface cleaner and easier to manage.

---

# 🌍 Global Variables

```python
reps = 0
timer = None
```

### `reps`

Tracks total completed sessions.

Example:

```text
1 → Work
2 → Short Break
3 → Work
4 → Short Break
...
8 → Long Break
```

### `timer`

Stores the ID returned by `window.after()` so the timer can be cancelled when Reset is pressed.

---

# ▶️ `start_timer()`

This function controls the complete Pomodoro cycle.

Main responsibilities:

* Increase session count
* Decide whether it's:

  * Work Session
  * Short Break
  * Long Break
* Start countdown
* Change title color

Logic:

```python
if reps % 8 == 0:
    Long Break
elif reps % 2 == 0:
    Short Break
else:
    Work
```

---

# ⏳ `count_down()`

This function updates the timer every second.

Main tasks:

* Convert seconds into minutes
* Update timer text
* Call itself every second using `after()`
* Start the next session automatically
* Display completed work session check marks

Example:

```python
window.after(1000, count_down, count - 1)
```

`after()` schedules the function after **1000 milliseconds (1 second)**, creating a smooth countdown without freezing the GUI.

---

# 🔄 `reset_timer()`

Reset button performs the following actions:

* Stops running timer
* Resets countdown to **00:00**
* Changes title back to **Timer**
* Removes all check marks
* Resets session counter

---

# 🖼️ Canvas

Canvas is used to display:

* Tomato Image
* Countdown Text

```python
canvas.create_image(...)
canvas.create_text(...)
```

Unlike a Label, Canvas allows combining images and custom text at specific positions.

---

# 🏷️ Labels

Three labels are used:

### Title Label

Displays:

* Timer
* Work
* Break

depending on the current session.

### Timer Label

Displays the live countdown on the canvas.

### Check Marks Label

Shows completed work sessions:

```text
✔

✔✔

✔✔✔

✔✔✔✔
```

---

# 🎮 Buttons

### Start Button

Starts the Pomodoro timer.

```python
Button(command=start_timer)
```

### Reset Button

Stops everything and resets the application.

```python
Button(command=reset_timer)
```

---

# ⚙️ Timer Flow

```text
Start Button
      ↓
Increase reps
      ↓
Work / Break Decision
      ↓
Countdown Starts
      ↓
Timer Ends
      ↓
Next Session Starts Automatically
      ↓
Check Marks Updated
```

---

# 🧠 Important Concepts Learned

* Tkinter GUI Development
* Grid Layout Manager
* Labels
* Buttons
* Canvas
* Images
* Global Variables
* Countdown Timer
* Event Handling
* `window.after()`
* State Management
* Function Calls
* Conditional Logic
* Session Tracking

---

# 📸 Screenshot

*Add your Pomodoro App screenshots here.*

<img width="1015" height="709" alt="1" src="https://github.com/user-attachments/assets/75d1cc27-acd8-4cfa-ab4a-df14675c2ffb" />

<img width="1021" height="693" alt="2" src="https://github.com/user-attachments/assets/6360bbfb-0c1f-4463-a565-f18e7e9e21e3" />

---

# ✅ Key Takeaways

* Built a complete desktop GUI application using **Tkinter**
* Learned how to create a real-time countdown timer
* Used `window.after()` instead of loops for GUI updates
* Implemented automatic work and break session switching
* Used global variables to manage application state
* Displayed images using `Canvas`
* Updated widgets dynamically using `config()` and `itemconfig()`
* Learned how multiple Tkinter widgets work together to build a complete application

---

# 🚀 Practice Tasks

* 🔔 Add a notification sound when the timer finishes.
* 🎵 Play an alarm after every session.
* ⏸️ Add Pause and Resume buttons.
* ⏱️ Allow users to customize work and break durations.
* 🌙 Add Dark Mode support.
* 📊 Display total completed Pomodoro sessions.
* 💾 Save completed sessions using a text file.

---

# 🎯 Day 28 Summary

Day 28 introduced **GUI programming with Tkinter** through a practical Pomodoro Timer project. Instead of writing console programs, we learned how to build an interactive desktop application using widgets, images, buttons, countdown timers and event-driven programming.

This project is a great introduction to real-world GUI development and demonstrates how Python can be used to create useful productivity applications.
