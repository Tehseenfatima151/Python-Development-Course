# Day 72 — Data Exploration with Pandas

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

> This day marks the start of the **Data Science track** — moving from Flask/web dev into working with real datasets using **Pandas**.

## 📌 Project: Exploring a Student Dataset

A hands-on script exploring a small sample dataset (`students.csv`) using core Pandas operations — loading, inspecting, filtering, sorting, grouping, and cleaning data. All output was run and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Loading data with `read_csv()`
```python
import pandas as pd
data = pd.read_csv("students.csv")
```
This turns a CSV file into a **DataFrame** — pandas' core 2D table structure (rows + labeled columns), similar to an Excel sheet but manipulable in code.

### 2. First look at the data
```python
data.head()      # first 5 rows
data.shape        # (rows, columns) e.g. (12, 6)
data.columns       # list of column names
data.info()        # column data types + non-null counts
data.describe()     # mean, std, min, max, quartiles for numeric columns
```
`.describe()` is often the fastest way to sanity-check a dataset — e.g. spotting an impossible value (like a negative age) immediately.

### 3. Series vs DataFrame
Selecting **one** column returns a `Series` (1D); selecting a **list** of columns returns a `DataFrame` (2D) — this distinction affects which methods are available.

```python
data["gpa"]              # -> Series
data[["name", "gpa"]]     # -> DataFrame
```

### 4. Filtering rows with boolean conditions
Pandas filters using a "boolean mask" — a True/False Series that selects matching rows.

```python
data[data["gpa"] > 3.7]

# Multiple conditions need & / | (not "and"/"or") and parentheses around each condition
data[(data["major"] == "Data Science") & (data["gpa"] > 3.7)]
```

### 5. Sorting
```python
data.sort_values(by="gpa", ascending=False).head(3)
```

### 6. `loc` vs `iloc`
- **`iloc`** — selects by integer **position** (like list indexing): `data.iloc[0]` → first row, regardless of any index labels.
- **`loc`** — selects by **label** or boolean condition: `data.loc[data["city"] == "Lahore"]`.

```python
data.iloc[0]                                   # first row by position
data.loc[data["city"] == "Lahore", ["name"]]     # rows by condition, specific columns
```

### 7. Grouping & aggregating with `groupby()`
```python
data.groupby("major")["gpa"].mean().sort_values(ascending=False)
```
This splits the data into groups (one per unique `major`), computes the average GPA within each group, then combines the results — the classic "split-apply-combine" pattern.

```python
data["city"].value_counts()   # quick frequency count per category
```

### 8. Adding a computed column
```python
data["years_left_to_graduate"] = data["graduation_year"] - 2026
```
Pandas operations broadcast automatically across the whole column — no manual loop needed.

### 9. Checking data quality
```python
data.isna().sum()          # missing values per column
data.duplicated().sum()     # count of fully duplicate rows
```
Real-world datasets are rarely clean — checking for nulls/duplicates is a standard first step before any analysis.

---

## 📂 Project Structure
```
day72/
├── data_exploration.py
├── students.csv
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas
python data_exploration.py
```
The script prints each step's output to the terminal with labeled section headers, so you can follow along with what each pandas operation produces.

---

## ✅ Key Takeaways
- A DataFrame is pandas' core structure — think of it as a smart, code-manipulable spreadsheet.
- Selecting one column → `Series`; selecting multiple → `DataFrame`. This distinction matters for chained operations.
- Filtering uses boolean masks (`data[condition]`), and combining conditions needs `&`/`|` with parentheses, not Python's `and`/`or`.
- `loc` filters by **label/condition**, `iloc` filters by **integer position** — mixing them up is a very common beginner bug.
- `groupby()` follows "split → apply → combine": split into groups, apply an aggregate function, combine results into one output.
- Always check `.isna().sum()` and `.duplicated().sum()` early — clean data assumptions are usually wrong until verified.

## 📝 Practice Tasks
1. Add a new row to `students.csv` with a missing GPA value, then use `.fillna()` to fill it with the column's mean.
2. Find the city with the highest average GPA using `groupby()`.
3. Use `.apply()` with a custom function to classify each student as `"On Track"` or `"Behind"` based on `graduation_year`.
4. Export the `high_achievers` DataFrame (GPA > 3.7) to a new CSV using `.to_csv()`.
