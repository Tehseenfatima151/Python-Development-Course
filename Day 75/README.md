# Day 75 — Google Trends and Data Visualization

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Bitcoin — Search Interest vs Price

Exploring whether **Google search interest** (data from [trends.google.com](https://trends.google.com)) tracks real-world events — in this case, comparing monthly Bitcoin search interest against Bitcoin's price over the same period. This is the same pattern Angela Yu's course uses for Unemployment Rate and Tesla stock too.

All 3 charts were generated and verified locally before writing this README.

---

## 🧠 Concepts Covered

### 1. Converting text dates into real datetime objects
Google Trends exports dates as plain strings — pandas needs to know they're dates to sort, plot, or resample them correctly.

```python
df["month"] = pd.to_datetime(df["month"])
```
Without this conversion, matplotlib would treat dates as arbitrary text labels instead of understanding their chronological order and spacing.

### 2. Checking for missing data (very common in real Trends exports)
Google Trends often has gaps or `<1` values in raw exports. Always verify before analysis.

```python
df.isna().sum()
```

### 3. Correlation — do two trends move together?
`.corr()` calculates the **Pearson correlation coefficient**, a number from -1 to 1:
- **Close to +1** → both values tend to rise and fall together
- **Close to -1** → one rises while the other falls (inverse relationship)
- **Close to 0** → little to no linear relationship

```python
correlation = df["bitcoin_search_interest"].corr(df["bitcoin_price_usd"])
```
⚠️ Correlation is **not causation** — high search interest and high price moving together doesn't prove search volume *causes* price changes (or vice versa); both could be driven by the same underlying news/hype.

### 4. Dual-axis line chart — comparing two different scales
Search interest (0–100) and price (thousands of dollars) live on completely different scales. Plotting both on the same y-axis would flatten one of them. `twinx()` creates a second y-axis sharing the same x-axis.

```python
fig, ax1 = plt.subplots()
ax1.plot(df["month"], df["bitcoin_search_interest"], color="teal")

ax2 = ax1.twinx()   # shares the x-axis, independent y-axis
ax2.plot(df["month"], df["bitcoin_price_usd"], color="orange")
```
This is the single most important chart type for this kind of "does search interest track a real metric" analysis.

### 5. Scatter plot — visualizing correlation directly
While the dual-axis chart shows the trend *over time*, a scatter plot removes the time dimension and shows the direct relationship between the two variables — a tighter diagonal cluster means stronger correlation.

```python
plt.scatter(df["bitcoin_search_interest"], df["bitcoin_price_usd"])
```

### 6. Rolling averages — smoothing out noisy data
Monthly search interest can be jumpy. A **rolling average** smooths short-term noise so the underlying trend is easier to see.

```python
df_sorted = df.sort_values("month").set_index("month")
rolling = df_sorted["bitcoin_search_interest"].rolling(window=3).mean()
```
`window=3` averages each point with the 2 before it — a classic technique also used in stock charts ("3-month moving average").

### 7. Formatting date axes properly
```python
fig.autofmt_xdate(rotation=45)   # auto-rotates date labels so they don't overlap
```

---

## 📂 Project Structure
```
day75/
├── google_trends_analysis.py
├── bitcoin_search_trends.csv
├── chart_1_dual_axis_trend.png
├── chart_2_correlation_scatter.png
├── chart_3_rolling_average.png
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas matplotlib
python google_trends_analysis.py
```
Prints correlation stats to the terminal and saves 3 `.png` charts to the folder.

> **Note on the dataset:** `bitcoin_search_trends.csv` here is realistic sample data built to match the structure of a real Google Trends export merged with price data. For the actual project, export real search interest data from [trends.google.com](https://trends.google.com) (search "Bitcoin", download CSV) and merge it with real historical price data (e.g. from Yahoo Finance) — the script's column names/logic stay the same.

---

## 🖼️ Sample Output
<img width="659" height="403" alt="image" src="https://github.com/user-attachments/assets/6b40d65a-6423-4e56-9998-24d8dbfe9a78" />


---

## ✅ Key Takeaways
- Always convert date strings to real `datetime` objects with `pd.to_datetime()` before any time-series work.
- `twinx()` is essential when comparing two metrics on very different scales on one time axis.
- A high correlation coefficient shows two variables move together — it does **not** prove one causes the other.
- Rolling averages smooth noisy real-world data so the underlying trend is easier to read.
- Real Google Trends exports are messier than clean sample data — always check for missing/`<1` values before analyzing.

## 📝 Practice Tasks
1. Download a real Google Trends CSV (e.g. search interest for "unemployment benefits") and merge it with real unemployment rate data from FRED (fred.stlouisfed.org).
2. Try `window=6` instead of `window=3` for the rolling average and compare how much smoother the line becomes.
3. Add a second correlation calculation using Spearman's method (`df[...].corr(df[...], method="spearman")`) and compare it to Pearson's.
4. Highlight a specific date range on the dual-axis chart (e.g. `plt.axvspan()`) to mark a real-world event, like a major Bitcoin price crash.
