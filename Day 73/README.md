# Day 73 — Data Visualization with Matplotlib

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Visualizing the Student Dataset

Building on Day 72's Pandas exploration, this project turns the same `students.csv` dataset into 6 different chart types using **Matplotlib** — the foundational plotting library most other Python visualization tools (Seaborn, Pandas' `.plot()`) are built on top of.

All 6 charts were generated and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. The basic Matplotlib workflow
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))   # create a figure with a specific size
plt.plot(x, y)                 # draw on it
plt.title("...")
plt.xlabel("...")
plt.ylabel("...")
plt.savefig("chart.png")       # save to file
plt.close()                    # free memory before the next chart
```
`plt.show()` opens an interactive window — but in a terminal/server environment without a display, `plt.savefig()` is used instead to write the chart directly to a `.png` file.

### 2. Line chart — showing a trend
```python
sorted_data = data.sort_values(by="gpa")
plt.plot(sorted_data["name"], sorted_data["gpa"], marker="o")
```
Line charts are best for showing an **ordered progression** — here, GPA sorted from lowest to highest makes the spread easy to read at a glance.

### 3. Bar chart — comparing categories
```python
avg_gpa = data.groupby("major")["gpa"].mean()
plt.bar(avg_gpa.index, avg_gpa.values)
```
Bar charts are the go-to for comparing a metric **across distinct categories** (here, average GPA per major). Height directly represents magnitude, which is easy for readers to compare visually.

### 4. Pie chart — showing proportions of a whole
```python
city_counts = data["city"].value_counts()
plt.pie(city_counts.values, labels=city_counts.index, autopct="%1.1f%%")
```
`autopct="%1.1f%%"` auto-labels each slice with its percentage. Pie charts work best with a **small number of categories** — too many slices become unreadable.

### 5. Scatter plot — relationship between two numeric variables
```python
plt.scatter(data["age"], data["gpa"])
```
Used to visually check if two variables might be **correlated** — e.g., does age relate to GPA at all in this dataset? (In this sample data, not really — the points are fairly scattered.)

### 6. Histogram — distribution of a single variable
```python
plt.hist(data["gpa"], bins=6)
```
Unlike a bar chart (categories), a histogram groups **continuous numeric values** into ranges ("bins") and shows how many data points fall into each range — revealing the overall shape of the distribution.

### 7. Subplots — multiple charts in one figure
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].bar(...)
axes[1].pie(...)
plt.tight_layout()
```
`subplots(rows, cols)` creates a grid of chart "slots" (`axes`) you can plot into individually — useful for side-by-side comparisons in one image instead of scrolling through separate charts.

### 8. Styling essentials
- `color=` — hex codes or named colors for consistency
- `plt.xticks(rotation=45, ha="right")` — rotates long x-axis labels so they don't overlap
- `plt.tight_layout()` — auto-adjusts spacing so titles/labels don't get cut off
- `alpha=` — transparency, useful when points overlap in a scatter plot

---

## 📂 Project Structure
```
day73/
├── data_visualization.py
├── students.csv
├── chart_1_line_gpa.png
├── chart_2_bar_avg_gpa.png
├── chart_3_pie_by_city.png
├── chart_4_scatter_age_vs_gpa.png
├── chart_5_histogram_gpa.png
├── chart_6_subplots.png
└── README.md
```

## ▶️ How to Run
```bash
pip install matplotlib pandas
python data_visualization.py
```
This generates all 6 `.png` chart files in the same folder — no display/GUI required, since the script saves to file instead of calling `plt.show()`.

---

## 🖼️ Sample Output
<img width="659" height="498" alt="image" src="https://github.com/user-attachments/assets/92708f6f-d836-4bb5-b799-f61699717851" />


---

## ✅ Key Takeaways
- Chart type should match the question: **line** = trend, **bar** = category comparison, **pie** = proportions of a whole, **scatter** = relationship between two variables, **histogram** = distribution of one variable.
- `plt.savefig()` is the right choice over `plt.show()` when running scripts without a display (servers, some IDEs, automation).
- `plt.close()` after each chart prevents matplotlib from silently reusing/overlaying figures in a script that generates many charts.
- Pie charts lose readability past ~5-6 slices — a bar chart is usually a better choice for many categories.
- `plt.tight_layout()` is a small habit that fixes most "my labels got cut off" issues.

## 📝 Practice Tasks
1. Add a horizontal bar chart (`plt.barh()`) ranking students by GPA, top to bottom.
2. Add axis gridlines to the line chart using `plt.grid(True)` and compare readability.
3. Try a stacked bar chart showing student counts per major, split by city.
4. Recreate `chart_2_bar_avg_gpa.png` using Pandas' built-in `.plot(kind="bar")` shortcut and compare how much code it saves vs raw Matplotlib.
