# Day 76— Beautiful Plotly Charts & Analysing the Android App Store

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Google Play Store Data Analysis

Analyzing a dataset of Android apps (category, rating, installs, size, price) using Pandas and advanced **Plotly** chart types — going beyond Day 74's basics into donut charts, box plots, bubble charts, and color-scaled bar charts. All 7 charts were generated and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Donut chart — Free vs Paid apps
```python
fig = px.pie(df, names="Type", hole=0.4)   # hole=0.4 turns a pie into a donut
fig.update_traces(textinfo="percent+label")
```
A donut chart is just a pie chart with a `hole` — often considered more readable since the center space can hold a label/total.

### 2. Sorted horizontal bar chart with a color scale
```python
fig = px.bar(
    x=category_counts.values, y=category_counts.index,
    orientation="h", color=category_counts.values,
    color_continuous_scale="Teal"
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
```
`color=` mapped to the same values being plotted adds a visual gradient — bars representing bigger numbers are automatically shaded darker/lighter, reinforcing the comparison at a glance. `categoryorder: "total ascending"` guarantees bars are sorted by size, not alphabetically.

### 3. Box plot — comparing distributions across categories
```python
fig = px.box(df, x="Category", y="Rating", color="Category")
```
Unlike a bar chart (which shows only one number per category, like an average), a **box plot** shows the full spread: median, quartiles, and outliers — revealing that two categories with the same *average* rating can have very different consistency.

### 4. Bubble chart — visualizing 3+ variables at once
```python
fig = px.scatter(
    df, x="Size_MB", y="Rating",
    size="Installs", color="Type",
    hover_name="App"
)
```
A bubble chart is a scatter plot where a **third variable controls dot size** — here, app size (x), rating (y), and install count (bubble size) are all visible in a single chart. `hover_name` makes each point show the app name on hover, essential for exploratory analysis with many data points.

### 5. Color-scaled bar chart using a secondary metric
```python
fig = px.bar(
    top_reviewed, x="Reviews", y="App", orientation="h",
    color="Rating", color_continuous_scale="Viridis"
)
```
This packs **two metrics into one chart**: bar length shows review count, while color shows rating — so you can spot, for example, a heavily-reviewed app with a mediocre rating at a glance.

### 6. Filtering before visualizing
```python
paid_apps = df[df["Type"] == "Paid"]
fig = px.scatter(paid_apps, x="Price", y="Rating", size="Installs", color="Category")
```
Not every chart needs the full dataset — filtering to just paid apps first makes the price-vs-rating relationship visible without free apps (`Price = 0`) cluttering the x-axis.

### 7. Checking data quality before analysis
```python
df.isna().sum()
df.duplicated(subset="App").sum()
```
Real Play Store exports often have missing ratings (new apps) or duplicate entries (an app listed under two categories) — always verify before drawing conclusions from category-level averages.

---

## 📂 Project Structure
```
day77/
├── play_store_analysis.py
├── apps.csv
├── chart_1_free_vs_paid.html
├── chart_2_apps_per_category.html
├── chart_3_avg_installs_by_category.html
├── chart_4_rating_boxplot.html
├── chart_5_bubble_size_rating_installs.html
├── chart_6_top10_reviewed.html
├── chart_7_paid_price_vs_rating.html
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas plotly
python play_store_analysis.py
```
Prints each analysis step to the terminal and generates 7 interactive `.html` charts — open any of them in a browser to hover, zoom, and explore individual apps.

> **Note on the dataset:** `apps.csv` here is a realistic 30-app sample built in the same structure as the real Google Play Store dataset used for this project (commonly sourced from Kaggle: *Google Play Store Apps*). Swap in the real CSV and the script's column names/logic stay the same — the real dataset just has ~10,000 rows instead of 30.

---

## ✅ Key Takeaways
- A donut chart (`hole=` parameter) is a simple, effective variation on a pie chart.
- Box plots reveal the *spread* of data, not just the average — two categories can tie on mean rating while differing wildly in consistency.
- Bubble charts (`size=`) let you visualize a third numeric dimension without needing a 3D plot.
- Mapping `color=` to a numeric column (not just a category) turns a simple bar/scatter chart into a two-metric visualization.
- Filter data *before* charting when the full dataset would clutter or distort the relationship you're trying to show (e.g. excluding free apps from a price analysis).
- Always run `isna().sum()` and `duplicated().sum()` before trusting category-level aggregates on a real-world dataset.

## 📝 Practice Tasks
1. Add a chart showing the correlation between `Reviews` and `Installs` — do heavily-reviewed apps also have the most installs?
2. Filter to just the `GAME` category and build a bubble chart comparing size, rating, and reviews within games only.
3. Add a `content_rating` breakdown — which content ratings (Everyone, Teen, Mature 17+) dominate the dataset?
4. Try `px.sunburst()` with `Category` and `Genre` as hierarchy levels for a nested category breakdown.
