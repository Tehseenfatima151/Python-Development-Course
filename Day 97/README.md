# Day 97 — Web Development Portfolio Project: Personal Portfolio Site

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Developer Portfolio Website

A single-file, fully responsive personal portfolio website — built with plain **HTML, CSS, and vanilla JavaScript** (no frameworks, no build step). Designed around a code-editor/terminal aesthetic that fits a software engineering identity: a live terminal-style hero, tab-styled navigation, and file-card-style project listings.

---

## 🎨 Design Direction

Rather than a generic template look, this design leans into the subject: a developer's actual daily environment — a code editor and terminal.

- **Palette:** deep navy-black background (`#0B0F19`), a cool teal accent (`#5EEAD4`) for primary actions/links, and a warm amber accent (`#FBBF24`) used sparingly for secondary emphasis (tags, terminal output highlights).
- **Typography:** `Space Grotesk` for headings (distinctive, geometric — reads as "engineered" rather than generic), `Inter` for body copy (highly readable), and `JetBrains Mono` for anything code-flavored — nav tabs, terminal text, skill tags — used functionally, not just decoratively.
- **Signature element:** the hero is a live terminal window running `whoami`, printing out identity/skills line-by-line like real shell output — this is the single most memorable/distinctive piece of the design.
- **Navigation** mimics editor tabs (`about.md`, `skills.json`, `projects/`, `contact.sh`) — a small detail that reinforces the theme without being gimmicky, since these labels double as real anchor links.

---

## 🧠 Concepts Covered

### 1. CSS custom properties (design tokens)
```css
:root{
  --bg:#0B0F19;
  --accent:#5EEAD4;
  --accent-amber:#FBBF24;
  --radius:10px;
}
```
Defining colors/spacing once at the root means changing a brand color later is a one-line edit, not a find-and-replace across the whole file.

### 2. Sticky navigation with a blur backdrop
```css
.navbar{
  position:sticky; top:0; z-index:50;
  background:rgba(11,15,25,0.85);
  backdrop-filter:blur(10px);
}
```
`backdrop-filter: blur()` creates the "frosted glass" effect seen in most modern apps — content scrolling underneath the nav is visible but softened, instead of a flat solid bar abruptly covering it.

### 3. CSS Grid for responsive layouts
```css
.hero-grid{ display:grid; grid-template-columns:1.1fr 0.9fr; gap:48px; }

@media (max-width:860px){ .hero-grid{ grid-template-columns:1fr; } }
```
Grid handles the two-column desktop layout; a single media query collapses it to one column on mobile — no separate mobile-specific markup needed.

### 4. A CSS-only blinking cursor animation
```css
.cursor{
  display:inline-block; width:3px; height:1em;
  background:var(--accent-amber);
  animation: blink 1s step-end infinite;
}
@keyframes blink{ 50%{ opacity:0; } }
```
`step-end` makes the opacity change happen instantly rather than fading — mimicking a real terminal cursor's on/off blink instead of a smooth pulse.

### 5. Accessible focus states
```css
:focus-visible{ outline:2px solid var(--accent); outline-offset:3px; }
```
`:focus-visible` (rather than `:focus`) shows the outline only for keyboard navigation, not every mouse click — meeting accessibility expectations without adding visual noise for mouse users.

### 6. Semantic anchor navigation
```html
<a class="tab" href="#projects">projects/</a>
...
<section id="projects">...</section>
```
Combined with `html { scroll-behavior: smooth; }`, this gives smooth in-page scrolling to any section using only native HTML/CSS — no JavaScript scroll library needed.

### 7. Mobile-first responsive breakpoints
```css
@media (max-width:760px){ .skill-groups{ grid-template-columns:1fr; } }
@media (max-width:700px){ .tabs{ display:none; } }
```
Different components collapse at different breakpoints based on when *they specifically* start looking cramped — rather than one single global breakpoint for the whole page.

---

## 📂 Project Structure
```
day83/
└── index.html      # everything — HTML, CSS, and structure in one file
```

## ▶️ How to Run
No build step, no dependencies — just open the file:
```bash
# Option 1: double-click index.html to open in your browser

# Option 2: serve it locally
python -m http.server 8000
# then visit http://localhost:8000
```

To make it a real live portfolio: push this file to a GitHub repo and enable **GitHub Pages** (Settings → Pages → deploy from `main` branch), or drag-and-drop the file onto [Netlify Drop](https://app.netlify.com/drop) for an instant live link.
<img width="1345" height="594" alt="image" src="https://github.com/user-attachments/assets/1eab0bd4-cdcd-48fa-a422-1966b28d9578" />
<img width="1353" height="596" alt="image" src="https://github.com/user-attachments/assets/ac8c0d9c-4c4e-443d-a98d-332455138453" />


---

## ✅ Key Takeaways
- A distinctive design idea (terminal-hero, editor-tab nav) makes a personal portfolio memorable — a generic hero + stats layout blends into every other portfolio a recruiter sees that day.
- CSS custom properties (`--variables`) turn a whole color/spacing scheme into a handful of editable values at the top of the file.
- `backdrop-filter: blur()` and `:focus-visible` are small, modern CSS features that make a hand-written site feel as polished as a framework-built one.
- CSS Grid + a couple of media queries is often enough for full responsiveness — no CSS framework required for a page this size.
- A portfolio site is itself a portfolio project — this file is something you can genuinely deploy and link from your resume/GitHub profile today.

## 📝 Practice Tasks
1. Replace the placeholder project links (`href="#"`) with real GitHub repo and live-demo URLs for your actual Day 61/64/66/69 projects.
2. Add a real working contact form (could POST to [Formspree](https://formspree.io/) for a no-backend solution).
3. Add a light/dark mode toggle using a CSS class swap and `localStorage` (or, since this project avoids localStorage per the artifact environment's rules, wire it up once deployed outside Claude).
4. Extend the terminal hero animation so it "types" the commands character-by-character with JavaScript, instead of showing the finished output immediately.
