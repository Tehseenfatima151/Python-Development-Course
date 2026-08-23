# Day 74 — Lego Analysis for Course

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Analyzing Lego Sets & Colors

Exploring a subset of the real **Rebrickable Lego dataset** (colors + sets) using Pandas for analysis and **Plotly** for interactive visualizations — a step up from Day 73's static Matplotlib charts. All 4 charts were generated and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Why Plotly instead of Matplotlib for this project
Plotly charts are **interactive** by default — hovering shows exact data values, and charts can be zoomed/panned in the browser. This matters for exploratory analysis where you want to inspect specific data points, not just see a static image.

```python
import plotly.express as px
fig = px.line(x=years, y=counts, title="Sets Released Per Year")
fig.write_html("chart.html")   # opens as an interactive page in any browser
```

### 2. Counting unique values
```python
colors["name"].nunique()          # how many unique Lego colors exist
colors["is_trans"].value_counts()  # transparent vs opaque color counts
```

### 3. Sets released per year — a `groupby` + line chart
```python
sets_per_year = sets.groupby("year")["set_num"].count()

fig = px.line(x=sets_per_year.index, y=sets_per_year.values,
              title="Number of Lego Sets Released Per Year")
```
This reveals how Lego's release volume has changed over decades — Rebrickable's full dataset (70,000+ sets) shows a sharp increase after the 2000s; even this small sample hints at the same pattern.

### 4. Scatter plot with a trendline — set complexity over time
```python
fig = px.scatter(sets, x="year", y="num_parts", trendline="ols")
```
`trendline="ols"` fits an **Ordinary Least Squares regression line** directly onto the scatter plot, making an upward/downward trend visually obvious instead of just eyeballing scattered points. (Requires the `statsmodels` package.)

### 5. Horizontal bar chart — ranking largest sets
```python
top_10 = sets.sort_values(by="num_parts", ascending=False).head(10)

fig = px.bar(top_10.sort_values("num_parts"), x="num_parts", y="name", orientation="h")
```
Sorting *before* plotting (ascending, since Plotly draws bottom-to-top) makes the largest set appear at the top of a horizontal bar chart — a common formatting gotcha worth knowing.

### 6. Pie chart of a boolean column
```python
colors["is_trans_label"] = colors["is_trans"].map({True: "Transparent", False: "Opaque"})
fig = px.pie(colors, names="is_trans_label")
```
Mapping `True`/`False` to readable labels first makes the chart legend far clearer than showing raw booleans.

### 7. Real-world dataset note
The full Rebrickable dataset also includes `themes.csv` and `inventories.csv`, which would let you answer richer questions (e.g. "which theme has the most parts on average?") via a **merge/join** across multiple CSVs — a natural next step once comfortable with single-table analysis.

---

## 📂 Project Structure
```
day74/
├── lego_analysis.py
├── colors.csv                       # sample subset (full dataset: rebrickable.com/downloads)
├── sets.csv                          # sample subset
├── chart_1_sets_per_year.html
├── chart_2_parts_trend.html
├── chart_3_top10_largest_sets.html
├── chart_4_trans_vs_opaque.html
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas plotly statsmodels
python lego_analysis.py
```
This prints each analysis step to the terminal and generates 4 interactive `.html` charts — open any of them directly in a browser to hover, zoom, and explore the data.

> **Note on the dataset:** `colors.csv` and `sets.csv` here are a small sample built in the same structure as the real Rebrickable data. For the full analysis (70,000+ real Lego sets), download the actual CSVs from https://rebrickable.com/downloads/ and drop them in this folder — the script's column names match, so no code changes are needed.

---


## ✅ Screenshoot
<img width="656" height="408" alt="image" src="https://github.com/user-attachments/assets/bb9b45ad-a83e-4e15-bf2e-bf6537075b15" />

---
## ✅ Key Takeaways
- Plotly's interactivity (hover, zoom) makes it better suited than Matplotlib for *exploring* data, while Matplotlib's static images are often better for reports/papers.
- `trendline="ols"` on a scatter plot is a quick way to visualize a trend without manually fitting a regression.
- Sort direction matters differently for horizontal bar charts — sort ascending so the largest value lands at the top.
- Boolean columns (`True`/`False`) should usually be mapped to readable labels before charting, not shown raw.
- Real data analysis projects often require joining multiple related CSVs (`sets.csv` + `themes.csv` + `inventories.csv`) — this project uses two tables as a first step toward that pattern.

## 📝 Practice Tasks
1. Download the real `themes.csv` from Rebrickable and merge it with `sets.csv` to find the theme with the most released sets.
2. Add a bar chart of colors added per decade (would need the real `colors.csv`, which includes a `year` column).
3. Convert `chart_3_top10_largest_sets` into a Matplotlib version and compare how much more code it takes vs the Plotly one-liner.
4. Filter `sets` to just Star Wars-themed sets (`theme_id == 158` in this sample) and chart their part-count trend separately.
