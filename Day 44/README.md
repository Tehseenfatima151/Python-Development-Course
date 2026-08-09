# Day 44 – Intermediate CSS & Color Game Project

## 📌 Overview
Is session mein humne **Intermediate CSS** concepts seekhe — positioning, pseudo-classes, transitions, aur responsive units. Iske baad humne ye concepts use kar ke ek **Color Game** banaya — jisme user ko diye gaye RGB value ke sath match karne wala sahi color box dhoondhna hota hai, aur click karne pe feedback milta hai.

---

## 1️⃣ CSS Positioning

```css
.box {
    position: relative;
    top: 10px;
    left: 20px;
}

.overlay {
    position: absolute;
    top: 0;
    right: 0;
}

.navbar {
    position: fixed;
    top: 0;
    width: 100%;
}
```

**Explanation:**
- `static` (default) — normal document flow, koi positioning nahi
- `relative` — apni original position se offset hota hai, lekin space wahi reserve rehti hai
- `absolute` — nearest **positioned** parent (jo `relative`/`absolute`/`fixed` ho) ke relative position hota hai
- `fixed` — screen ke ek jagah "chipak" jata hai, scroll karne pe bhi move nahi hota — navbars ke liye common

---

## 2️⃣ Pseudo-Classes — Interactive States

```css
button:hover {
    background-color: darkblue;
}

button:active {
    transform: scale(0.95);
}

input:focus {
    border-color: blue;
}

li:first-child {
    font-weight: bold;
}

li:nth-child(2) {
    color: red;
}
```

**Explanation:**
- `:hover` — mouse element ke upar ho tab
- `:active` — click hone ke exact moment pe
- `:focus` — input field select ho tab
- `:first-child`/`:nth-child()` — position ke hisaab se specific elements target karna

---

## 3️⃣ CSS Transitions — Smooth Animations

```css
button {
    background-color: steelblue;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
    background-color: darkblue;
    transform: scale(1.05);
}
```

**Explanation:** `transition` property batati hai ke kaunsi property kitne time mein aur kaise (easing) change ho — bina isके, hover effects instant/jerky lagte hain.

---

## 4️⃣ Responsive Units — px vs % vs vh/vw vs rem

```css
.box {
    width: 300px;
    width: 50%;
    height: 100vh;
    font-size: 1.5rem;
}
```

**Explanation:** `vh`/`vw` (viewport height/width) responsive designs ke liye useful hain. `rem` font sizes ke liye better hai kyunke ye scalable/accessible hota hai.

---

## 5️⃣ Building the Color Game

**Concept:** Screen pe ek target RGB value dikhti hai (jaise `RGB(180, 26, 90)`), aur 6 color boxes hote hain — sirf ek box us exact RGB value ka hai. User ko sahi box dhoondh kar click karna hota hai; sahi hone pe "Correct!" aur galat hone pe "Wrong! Try Again" show hota hai.

### `index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Color Game</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 id="game-status">Guess the Correct Color</h1>
    <div class="rgb-display" id="rgb-value">RGB(180, 26, 90)</div>

    <div class="squares-container">
        <div class="square" style="background-color: rgb(180, 26, 90);"></div>
        <div class="square" style="background-color: rgb(75, 120, 200);"></div>
        <div class="square" style="background-color: rgb(50, 180, 90);"></div>
        <div class="square" style="background-color: rgb(220, 90, 40);"></div>
        <div class="square" style="background-color: rgb(140, 60, 200);"></div>
        <div class="square" style="background-color: rgb(30, 30, 30);"></div>
    </div>

    <button id="new-game-btn" onclick="location.reload()">New Game</button>

    <script src="script.js"></script>
</body>
</html>
```

### `style.css`

```css
body {
    text-align: center;
    font-family: Arial, sans-serif;
    background-color: #232333;
    color: white;
    padding-top: 40px;
}

.rgb-display {
    font-size: 22px;
    margin-bottom: 30px;
    letter-spacing: 1px;
}

.squares-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
    max-width: 400px;
    margin: 0 auto;
}

.square {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.15s ease;
}

.square:hover {
    transform: scale(1.05);
}

.square:active {
    transform: scale(0.95);
}

#new-game-btn {
    margin-top: 30px;
    padding: 10px 25px;
    background-color: white;
    color: #232333;
    border: none;
    border-radius: 20px;
    font-size: 15px;
    cursor: pointer;
}
```

**Explanation:**
- `.square:hover` aur `:active` — pseudo-classes se click-feel dete hain
- `transition: transform 0.15s ease` — smooth scale animation
- `onclick="location.reload()"` — page ko reload kar deta hai, naya random game shuru karne ke liye

### `script.js`

```javascript
const correctColor = "rgb(180, 26, 90)";

const squares = document.querySelectorAll(".square");
const statusText = document.getElementById("game-status");

squares.forEach(function (square) {
    square.addEventListener("click", function () {
        const clickedColor = square.style.backgroundColor;

        if (clickedColor === correctColor) {
            statusText.textContent = "Correct!";
            document.body.style.backgroundColor = correctColor;
        } else {
            square.style.backgroundColor = "#232333";
            statusText.textContent = "Wrong! Try Again";
        }
    });
});
```

**Explanation:**
- `document.querySelectorAll(".square")` — sare `.square` class wale elements ek list ki soorat mein le leta hai
- `.forEach(function (square) {...})` — har square pe loop chalata hai (JavaScript ka `forEach` Python ke `for` loop jaisa hai)
- `addEventListener("click", function() {...})` — Python ke Tkinter `command=` jaisa hi concept, bas is dafa JavaScript ka native event-listener syntax
- Agar sahi color click ho: poori body ka background bhi us color mein badal jata hai
- Agar galat ho: wo box "disable" jaisa dark ho jata hai, taake dobara na chuna jaye

---

## ✅ Key Takeaways
- `position: relative/absolute/fixed` elements ko precisely place karne ke different tareeqe dete hain
- Pseudo-classes (`:hover`, `:active`, `:focus`, `:nth-child()`) bina JavaScript ke bhi interactive feel deti hain
- `transition` property se instant/jerky changes ko smooth animations mein badal sakte hain
- Responsive units (`vh`, `vw`, `%`, `rem`) fixed `px` se zyada flexible designs banate hain
- `querySelectorAll()` + `forEach()` JavaScript mein multiple elements pe loop chalane ka standard pattern hai
- `addEventListener()` JavaScript ka native event-handling tareeqa hai — inline `onclick` se zyada scalable

---

## 🔗 Practice Task
- Game ko "Easy Mode" (3 boxes) aur "Hard Mode" (6 boxes) mein divide karo
- Random target color generate karo har naye game ke liye (fixed value ki bajaye)
- Ek score counter add karo jo track kare kitne correct guesses huay

---

## 📸 Screenshot

<!-- Apna webpage ka screenshot yahan drag & drop karo -->
<img width="778" height="388" alt="image" src="https://github.com/user-attachments/assets/4227171c-b9b2-4c42-a542-c39f335c7673" />
