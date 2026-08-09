# Day 42 – Birthday Wish Website (HTML, CSS & JavaScript)

## 📌 Overview
Is session mein humne Day 41 ke HTML/CSS/JS basics ko practically use kar ke ek **Birthday Wish Website** banayi — ek fun, interactive webpage jo birthday wish show karti hai, aur button click hone pe ek surprise message reveal karti hai.

---

## 1️⃣ Project Structure

```
birthday_wish_website/
├── index.html
├── style.css
└── script.js
```

---

## 2️⃣ `index.html` — Page Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Happy Birthday!</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 id="greeting">Happy Birthday!</h1>
        <p id="wish-text">Click the button for a special surprise!</p>
        <button onclick="revealSurprise()">Click Me!</button>
        <p id="surprise-message" class="hidden"></p>
    </div>

    <script src="script.js"></script>
</body>
</html>
```

**Explanation:**
- `<div class="container">` — ek wrapper jo poore content ko group karta hai (styling ke liye useful)
- `id="surprise-message"` — ye paragraph shuru mein hidden hota hai, JavaScript se dikhaya jayega

---

## 3️⃣ `style.css` — Styling

```css
body {
    text-align: center;
    font-family: 'Comic Sans MS', sans-serif;
    background: linear-gradient(135deg, #ff9a9e, #fecfef);
    padding-top: 100px;
    margin: 0;
}

.container {
    background: white;
    display: inline-block;
    padding: 40px 60px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

h1 {
    color: #e7305b;
}

button {
    padding: 12px 25px;
    background-color: #e7305b;
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 15px;
}

button:hover {
    background-color: #c41f45;
}

.hidden {
    display: none;
}

.visible {
    display: block;
    margin-top: 20px;
    font-size: 20px;
    color: #375362;
    font-weight: bold;
}
```

**Explanation:**
- `linear-gradient()` — background ko ek smooth color-transition deta hai (pink shades), simple solid color se zyada visually appealing
- `.hidden` / `.visible` — do CSS classes jo `display: none`/`display: block` toggle karti hain — JavaScript inhi classes ko switch karega

---

## 4️⃣ `script.js` — Interactivity

```javascript
function revealSurprise() {
    const surpriseMessage = document.getElementById("surprise-message");
    surpriseMessage.innerHTML = "Wishing you a year full of happiness and success!";
    surpriseMessage.classList.remove("hidden");
    surpriseMessage.classList.add("visible");
}
```

**Explanation:**
- `document.getElementById("surprise-message")` — us element ko "grab" karta hai
- `.innerHTML = "..."` — uske andar naya text daal deta hai
- `classList.remove("hidden")` aur `classList.add("visible")` — CSS classes ko JavaScript se dynamically switch karta hai, is se element show ho jata hai

---

## 5️⃣ Example Flow

1. Page load hone pe: greeting + button dikhta hai, surprise message hidden hota hai
2. User button click karta hai
3. `revealSurprise()` function chalta hai
4. Hidden paragraph visible ho jata hai, ek naya birthday message ke sath

---

## 📸 Screenshot

<!-- Apna webpage ka screenshot yahan drag & drop karo -->

<img width="902" height="614" alt="image" src="https://github.com/user-attachments/assets/e2382553-2787-4bf6-a1ad-81a280e4c07c" />

---

## ✅ Key Takeaways
- HTML structure banata hai, CSS usse style karta hai, aur JavaScript usse interactive banata hai — teeno mil kar poora experience dete hain
- `classList.add()`/`classList.remove()` se CSS classes ko dynamically toggle karna, elements show/hide karne ka clean tareeqa hai
- `linear-gradient()` jaisi CSS properties simple styling ko visually rich bana deti hain bina extra images ke
- `onclick` attribute JavaScript function ko HTML se seedha connect karta hai — bilkul Tkinter ke `command=` jaisa concept

---

## 🔗 Practice Task
- Multiple surprise messages add karo jo random show hon har baar button dabane pe
- Ek confetti/balloon animation add karo (CSS animations ya simple JS se)
- User se naam input lene do aur usi naam ke sath personalized wish show karo
