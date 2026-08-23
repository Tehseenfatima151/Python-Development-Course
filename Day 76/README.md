# Day 76 — Computation with NumPy and N-Dimensional Arrays

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: NumPy Fundamentals — Arrays, Vectorization & Broadcasting

A hands-on script covering NumPy's core building blocks — the foundation that Pandas, Matplotlib, and virtually every other Python data science library is built on top of. All 10 sections were run and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Creating arrays
```python
np.array([1, 2, 3])            # from a Python list
np.zeros((2, 3))                 # 2x3 array of zeros
np.ones((3, 2))                  # 3x2 array of ones
np.arange(0, 20, 2)               # like range(), but returns an array
np.linspace(0, 1, 5)              # 5 evenly spaced values between 0 and 1
```

### 2. Shape, dimensions, and reshaping
Every array has a `.shape` (size along each dimension) and `.ndim` (number of dimensions).
```python
matrix = np.arange(1, 13)         # shape (12,), ndim 1
matrix.reshape(3, 4)               # shape (3, 4), ndim 2
matrix.reshape(2, 2, 3)            # shape (2, 2, 3), ndim 3 — an "N-dimensional array"
```
`reshape()` doesn't change the data — it just changes how the same 12 numbers are organized/viewed. The total element count must stay the same (3×4=12, 2×2×3=12).

### 3. Indexing and slicing (row, column style)
```python
grid[1, 2]        # single element: row 1, column 2
grid[0, :]         # entire row 0
grid[:, 1]         # entire column 1
grid[0:2, 1:3]      # sub-grid: rows 0-1, columns 1-2
```
This `[row, column]` syntax is a big upgrade over Python's nested-list indexing (`grid[1][2]`) — much closer to how math notation describes matrices.

### 4. Vectorized operations — no loops needed
```python
a + b     # element-wise addition
a * b     # element-wise multiplication
a ** 2    # element-wise power
```
These apply the operation to *every element at once* — this is the core idea behind "vectorization."

### 5. Why NumPy is faster than plain Python loops
Squaring 1,000,000 numbers:
```python
squared_list = [x ** 2 for x in python_list]   # pure Python loop
squared_array = numpy_array ** 2                 # NumPy vectorized
```
**Measured result on this run: NumPy was ~6.6x faster.** NumPy arrays are stored as contiguous blocks of a single data type in memory (unlike Python lists, which store pointers to separate objects) and operations run in optimized, compiled C code under the hood — not Python's slower interpreted loop.

### 6. Boolean indexing — filtering without loops
```python
temps[temps > 25]                    # only values matching the condition
np.sum(temps > 25)                    # count of matches (True counts as 1)
np.where(temps > 25, "Hot", "Mild")    # conditional labeling, element-wise
```
`temps > 25` itself returns an array of `True`/`False` values — that boolean array is then used to filter the original array.

### 7. Aggregate/statistical functions
```python
np.mean(scores)
np.median(scores)
np.std(scores)     # standard deviation
np.min(scores) / np.max(scores)
np.argmax(scores)   # INDEX of the maximum value (not the value itself)
```

### 8. Axis-based aggregation on 2D arrays
The `axis` parameter controls whether you aggregate **across rows** or **across columns**:
```python
sales.sum(axis=1)   # one total PER ROW (sum across columns)
sales.sum(axis=0)   # one total PER COLUMN (sum across rows)
```
This trips up most beginners at first — `axis=0` moves *down* the rows (collapsing them into one row of column totals), `axis=1` moves *across* the columns (collapsing them into one column of row totals).

### 9. Broadcasting
```python
prices - (prices * 10 / 100)
```
NumPy automatically "stretches" the smaller value (`10`) to match the shape of `prices` and applies the operation element-wise — no manual loop or repeating the number into an array first. This is called **broadcasting**, and it's one of NumPy's most powerful features.

### 10. Random number generation
```python
rng = np.random.default_rng(seed=42)   # modern, recommended way (vs np.random.seed())
rng.integers(1, 100, size=5)
rng.random(5)
```
Using a `seed` makes random output **reproducible** — the same seed always produces the same "random" numbers, useful for debugging and sharing reproducible examples.

---

## 📂 Project Structure
```
day76/
└── numpy_computation.py
```

## ▶️ How to Run
```bash
pip install numpy
python numpy_computation.py
```
Runs all 10 sections in order, printing labeled output for each — including a live timing comparison between a Python loop and the equivalent NumPy operation.

---

## ✅ Key Takeaways
- NumPy arrays are faster than Python lists for numeric work because they store data in a fixed, contiguous block and run operations in compiled code, not the Python interpreter.
- `reshape()` reorganizes the *same* data into new dimensions — the total number of elements must match before and after.
- `axis=0` aggregates down columns (one result per column); `axis=1` aggregates across rows (one result per row) — worth double-checking every time, since it's easy to mix up.
- Boolean indexing (`arr[arr > x]`) replaces manual filtering loops entirely.
- Broadcasting lets NumPy apply a single value (or smaller array) across a larger array automatically, without writing a loop.
- `np.random.default_rng(seed=...)` is the modern, recommended way to generate reproducible random numbers (over the older `np.random.seed()`).

## 📝 Practice Tasks
1. Create a 4x4 matrix using `np.arange(16).reshape(4, 4)` and extract just its diagonal using `np.diag()`.
2. Time squaring 5,000,000 numbers instead of 1,000,000 — does NumPy's speed advantage grow or shrink?
3. Use boolean indexing to replace every negative number in `np.array([3, -2, 5, -8, 1])` with `0`.
4. Create two 3x3 matrices and try both `@` (matrix multiplication) and `*` (element-wise multiplication) — print both results and explain the difference.
