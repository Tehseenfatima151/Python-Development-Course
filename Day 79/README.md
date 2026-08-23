# Day 79 — Analysing the Nobel Prize with Plotly, Seaborn and Matplotlib

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Nobel Prize Winners Analysis

Analyzing 200 Nobel Prize laureates (1970–2023) — exploring gender gaps, age at award, and which countries dominate — using **all three** major Python visualization libraries in one project, each chosen for what it does best. All 7 charts were generated and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Choosing the right library for the job
This project intentionally uses all three, matched to their strengths:
- **Matplotlib** — simple, direct charts (a quick pie chart)
- **Seaborn** — statistical charts with built-in grouping (`hue=`), distributions, boxplots
- **Plotly** — interactive charts for exploring many categories (hover to see exact values)

### 2. Overall gender breakdown (Matplotlib)
```python
gender_counts = df["gender"].value_counts()
plt.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%")
```
**Result on this dataset: 87% Male, 13% Female** — reflecting the real, well-documented historical gender gap in Nobel Prizes.

### 3. Gender gap over time (Seaborn grouped bar chart)
```python
df["decade"] = (df["year"] // 10) * 10
gender_by_decade = df.groupby(["decade", "gender"]).size().reset_index(name="count")

sns.barplot(data=gender_by_decade, x="decade", y="count", hue="gender")
```
Grouping by **decade** turns 50+ years of individual data points into a readable trend — `hue="gender"` automatically splits each decade's bar into male/female side-by-side.

### 4. Age distribution with a KDE overlay (Seaborn)
```python
sns.histplot(df["age_at_award"], bins=20, kde=True)
```
`kde=True` overlays a smooth **Kernel Density Estimate** curve on top of the histogram bars — showing the distribution's overall shape without the "choppiness" that bin width alone can create.

**Result: mean age at award ≈ 60 years**, median also 60 — a fairly symmetric, centered distribution in this dataset.

### 5. Top countries — interactive Plotly bar chart
```python
fig = px.bar(x=top_countries.values, y=top_countries.index, orientation="h",
             color=top_countries.values, color_continuous_scale="Teal")
```
With 12+ countries in the dataset, Plotly's interactivity (hovering to see exact laureate counts) is more useful here than a static chart — especially once real data has 60+ countries.

### 6. Stacked bar chart — category breakdown per country (Plotly)
```python
fig = px.bar(category_country_top5, x="laureate_country", y="count",
             color="category", barmode="stack")
```
`barmode="stack"` shows both the **total** laureates per country (full bar height) and the **category breakdown within that total** (colored segments) — two insights in one chart.

### 7. Prizes over time by category (Plotly multi-line)
```python
fig = px.line(prizes_per_year_category, x="year", y="count", color="category")
```
Plotly automatically draws one line per category and builds a clickable legend — clicking a category in the legend toggles that line on/off, useful for isolating one trend in a busy chart.

### 8. Age by category — Seaborn boxplot with custom ordering
```python
order = df.groupby("category")["age_at_award"].median().sort_values().index
sns.boxplot(data=df, x="category", y="age_at_award", order=order, hue="category", legend=False)
```
Sorting categories by their **median** age (rather than alphabetically) makes the boxplot itself tell a story left-to-right — e.g. if Literature laureates tend to be older than Physics laureates, that pattern is immediately visible in the ordering.

---

## 📂 Project Structure
```
day79/
├── nobel_analysis.py
├── nobel_prize_winners.csv
├── chart_1_gender_pie_matplotlib.png
├── chart_2_gender_by_decade_seaborn.png
├── chart_3_age_distribution_seaborn.png
├── chart_4_top_countries_plotly.html
├── chart_5_category_by_country_plotly.html
├── chart_6_prizes_over_time_plotly.html
├── chart_7_age_by_category_seaborn.png
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas seaborn matplotlib plotly
python nobel_analysis.py
```
Prints stats to the terminal, saves 4 static `.png` charts (Matplotlib/Seaborn) and 3 interactive `.html` charts (Plotly).

> **Note on the dataset:** `nobel_prize_winners.csv` here is a realistic 200-laureate sample built to match the structure of the real dataset used for this project. The real Nobel Prize dataset (all ~1000 laureates since 1901) is available via the [official Nobel Prize API](https://www.nobelprize.org/organization/developer-zone-2/) or on Kaggle — the script's column names/logic stay the same either way.

---
## ✅ Screenshoot
<img width="657" height="481" alt="image" src="https://github.com/user-attachments/assets/7c63894e-b934-49d7-8b28-831f3911da88" />
---

## ✅ Key Takeaways
- Different libraries suit different jobs on the same project: Matplotlib for quick static charts, Seaborn for statistical grouping/distributions, Plotly for interactive exploration of many categories.
- `hue=` in Seaborn is the fast way to split any chart by a categorical variable — no manual loop needed.
- `kde=True` on a histogram reveals the distribution's shape more clearly than bins alone, especially with a moderate sample size.
- `barmode="stack"` in Plotly packs a total AND a breakdown into one bar chart.
- Sorting categorical axes by a meaningful statistic (like median) instead of alphabetically often makes a chart tell its own story.

## 📝 Practice Tasks
1. Add a chart comparing average age at award for Male vs Female laureates — has the gap changed over time?
2. Use `px.choropleth()` to map laureate counts onto a world map by country.
3. Calculate the "female percentage per decade" as a single trend line instead of grouped bars, using `sns.lineplot()`.
4. Filter the dataset to just the `Peace` category and explore whether age or country patterns differ from the overall dataset.
