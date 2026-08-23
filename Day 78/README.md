# Day 78 — Linear Regression and Data Visualization with Seaborn

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Predicting House Prices

Building a **Linear Regression** model (with scikit-learn) to predict house prices from square footage, bedrooms, age, and distance to city — using **Seaborn** for statistical visualization along the way. The model was actually trained and evaluated; results below are real output, not placeholders.

---

## 🧠 Concepts Covered

### 1. Seaborn vs Matplotlib
Seaborn is built on top of Matplotlib but specializes in **statistical** visualizations — it needs far less code for things like regression lines, distributions, and correlation heatmaps.

```python
import seaborn as sns
sns.set_style("whitegrid")   # one line for a clean default look
```

### 2. Correlation — which features actually matter?
Before building a model, checking correlation with the target variable (`price`) shows which features are worth including.

```python
correlations = df.corr(numeric_only=True)["price"].sort_values(ascending=False)
```
**Result on this dataset:** `sqft` (0.98) and `bedrooms` (0.89) correlate strongly with price; `age_years` (0.03) and `distance_to_city_km` (0.06) barely correlate at all — a useful signal before modeling.

### 3. Heatmap — visualizing the full correlation matrix
```python
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
```
`annot=True` prints the actual correlation number inside each cell — much faster to scan than a plain color grid.

### 4. Jointplot — scatter + regression line + distributions, in one chart
```python
sns.jointplot(data=df, x="sqft", y="price", kind="reg")
```
`kind="reg"` overlays a best-fit regression line directly on the scatter plot, and adds histograms of each variable along the margins — three insights in a single chart.

### 5. Pairplot — every feature against every other, automatically
```python
sns.pairplot(df, corner=True)
```
Instead of manually creating a scatter plot for every feature combination, `pairplot()` generates the entire grid at once — `corner=True` skips the redundant upper-triangle duplicates.

### 6. Boxplot — price spread grouped by a category
```python
sns.boxplot(data=df, x="bedrooms", y="price", hue="bedrooms", palette="viridis")
```

### 7. Splitting data into training and testing sets
A model must be evaluated on data it has **never seen** — otherwise it could just be memorizing, not learning a real pattern.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
`test_size=0.2` holds back 20% of the data purely for evaluation. `random_state=42` makes the split reproducible.

### 8. Training a Linear Regression model
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```
Linear Regression finds the best-fit weight (`coefficient`) for each feature that minimizes prediction error across the training data.

**Result on this dataset:**
```
sqft                 :        120.64   -> each extra sqft adds ~$120 to price
bedrooms             :      8,175.76   -> each extra bedroom adds ~$8,176
age_years            :     -1,342.41   -> each year older subtracts ~$1,342
distance_to_city_km  :     -1,150.30   -> each km further subtracts ~$1,150
intercept            :     52,401.63   -> base price with all features at 0
```

### 9. Evaluating with MAE and R²
```python
from sklearn.metrics import mean_absolute_error, r2_score

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
```
- **MAE (Mean Absolute Error)** — on average, how far off predictions are, in the same units as the target (dollars here).
- **R² Score** — how much of the variation in price the model explains; 1.0 = perfect, 0 = no better than always guessing the average.

**Result on this dataset: MAE = $15,946, R² = 0.981** — the model explains ~98% of price variation on unseen test data (this sample dataset was intentionally built with a strong linear relationship for teaching purposes).

### 10. Predicting on brand-new data
```python
new_house = pd.DataFrame([{"sqft": 2200, "bedrooms": 3, "age_years": 5, "distance_to_city_km": 8.0}])
model.predict(new_house)
```
Once trained, the model can predict a price for a house it has never seen — output on this run: **$326,416.97**.

---

## 📂 Project Structure
```
day78/
├── housing_regression.py
├── housing.csv
├── chart_1_correlation_heatmap.png
├── chart_2_jointplot_sqft_vs_price.png
├── chart_3_pairplot.png
├── chart_4_boxplot_bedrooms.png
├── chart_5_predicted_vs_actual.png
└── README.md
```

## ▶️ How to Run
```bash
pip install pandas seaborn matplotlib scikit-learn
python housing_regression.py
```
Prints correlation stats, model coefficients, and evaluation metrics to the terminal, and saves 5 charts to the folder.

---

## 🖼️ Sample Output

<img width="640" height="460" alt="image" src="https://github.com/user-attachments/assets/406ec116-299e-42fc-9c91-4883083ab0bb" />

---

## ✅ Key Takeaways
- Check correlation with the target variable before modeling — weak features (`age_years`, `distance_to_city_km` here) may add little predictive value.
- Seaborn's `jointplot()` and `pairplot()` replace many lines of manual Matplotlib code for common statistical charts.
- Always split data into train/test sets — evaluating on training data alone hides overfitting.
- **MAE** tells you the average error in real units (dollars); **R²** tells you the proportion of variance explained — use both, they answer different questions.
- Linear Regression coefficients are directly interpretable: each one tells you the dollar impact of a one-unit change in that feature, holding others constant.

## 📝 Practice Tasks
1. Remove `age_years` and `distance_to_city_km` from the model (since they barely correlate with price) and check if R² changes much.
2. Try `sns.lmplot()` instead of `jointplot()` for the sqft-vs-price relationship and compare the output.
3. Add a `neighborhood` categorical column to the dataset and encode it with `pd.get_dummies()` before including it in the model.
4. Compare this Linear Regression's R² against a `RandomForestRegressor` from scikit-learn on the same data.
