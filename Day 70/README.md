# Day 70 — Git, GitHub and Version Control

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

> **Note:** Day 70 is a tools/theory day, not a coding project. There's no Flask app for this day — instead, this README documents Git & GitHub fundamentals, and includes a reusable `.gitignore` file for Python/Flask projects.

---

## 🧠 Concepts Covered

### 1. What Git actually is (vs GitHub)
- **Git** — a version control *tool* that runs locally on your computer. It tracks every change to your files over time, so you can go back to any previous state.
- **GitHub** — a *website* that hosts Git repositories online, so you can back up your code, share it, and collaborate with others. Git can be used with or without GitHub.

### 2. The core Git workflow
```bash
git init                     # turn a folder into a Git repository
git status                   # see what's changed / staged / untracked
git add <file>                # stage a specific file for the next commit
git add .                     # stage everything changed in this folder
git commit -m "message"       # save a snapshot of staged changes
git log                       # view commit history
```
A **commit** is a saved checkpoint — you can always return to it later even if you break something afterward.

### 3. Connecting a local repo to GitHub
```bash
git remote add origin https://github.com/username/repo-name.git
git branch -M main
git push -u origin main       # first push: also sets 'origin main' as default
git push                      # every push after that
```
`git clone <url>` does the reverse — downloads an existing GitHub repo to your computer.

### 4. Pulling changes down
```bash
git pull                      # fetch + merge latest changes from GitHub
```
Important when working across multiple computers, or collaborating with others — always `pull` before starting new work to avoid conflicts.

### 5. Branches — working without breaking `main`
A branch is a parallel version of the codebase. You can experiment freely on a branch without touching the stable `main` branch.

```bash
git branch feature-login        # create a new branch
git checkout feature-login      # switch to it
git checkout -b feature-login   # create + switch in one command

git checkout main               # switch back to main
git merge feature-login         # bring the branch's changes into main
```

### 6. `.gitignore` — keeping junk out of your repo
Certain files should **never** be pushed to GitHub: virtual environments, cache files, secret keys, database files with real data, IDE settings. A `.gitignore` file tells Git to skip them automatically.

```
venv/
__pycache__/
.env
*.db
```
Without this, repos get bloated, slow, and can accidentally leak secrets (like API keys) publicly.

### 7. Commit messages that actually help
- ❌ `"fixed stuff"`, `"asdf"`, `"final final v2"`
- ✅ `"Fix login redirect bug when session expires"`, `"Add Flask-WTF form validation for cafe form"`

Good commit messages make it possible to understand your own project's history months later — especially useful across a 100-day project like this one.

### 8. Undoing mistakes
```bash
git checkout -- <file>          # discard uncommitted changes to a file
git reset --soft HEAD~1          # undo the last commit, keep the changes staged
git revert <commit-hash>         # safely undo a commit by creating a new "opposite" commit
```
`git revert` is safer than `reset` on shared/pushed history, since it doesn't rewrite what others may have already pulled.

---

## 📂 Files in This Folder
```
day70/
├── README.md
└── .gitignore      # reusable template for Python/Flask projects
```

## ✅ Key Takeaways
- Git tracks changes locally through **commits**; GitHub is where those commits get backed up and shared.
- `add` → `commit` → `push` is the core daily loop — `pull` first when working across machines or with others.
- Branches let you experiment safely without breaking a working `main` branch.
- A proper `.gitignore` protects against accidentally leaking secrets and bloating the repo with junk files (`venv/`, `.db`, `__pycache__/`).
- Clear, specific commit messages are a habit worth building early — future-you (and anyone reviewing your code) will thank you.

## 📝 Practice Tasks
1. Go back through your last 5 GitHub commits on this course repo — rewrite what their messages *should* have said if they were vague.
2. Add the `.gitignore` from this folder to every existing Day 6X Flask project folder that doesn't have one yet.
3. Practice creating a branch, making a small change, and merging it back into `main` on a throwaway test repo.
4. Check if any of your pushed repos accidentally include a `venv/` folder or `instance/*.db` file — if so, remove and add them to `.gitignore` going forward.
