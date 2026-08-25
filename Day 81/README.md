# 🚀 Day 81 — House Price Prediction

> **Python Development Journey | 100 Days of Code 🐍**

Welcome to **Day 81** of my Python Development Journey!

For Day 81, I built **PropVal.AI — an AI-Powered House Price Predictor**, a complete Machine Learning and Flask-based web application that predicts house prices based on property features such as area, bedrooms, bathrooms, and location.

This project helped me move from simply training ML models to building a **complete end-to-end Machine Learning application** with a web interface, REST API, model evaluation, data visualization, and persistent model deployment.

---

## 🏠 Project Overview

**PropVal.AI** is a Pakistani real-estate price prediction platform powered by Machine Learning.

Users can enter:

* 📍 Location
* 📐 Property Area
* 🛏️ Number of Bedrooms
* 🛁 Number of Bathrooms

and receive an estimated property value in **PKR**.

The application uses a trained **Random Forest Regressor** selected after benchmarking it against Linear Regression.

> ⚠️ **Dataset Note:** The housing dataset used in this project is synthetically generated for educational and Machine Learning demonstration purposes. It does not represent official live Pakistani real-estate market data.

---

## 🎯 What I Learned

Through this project, I practiced:

* Loading and processing datasets with Pandas
* Data preprocessing
* One-Hot Encoding
* Feature transformation
* Train/Test splitting
* Regression Machine Learning
* Model comparison
* Model evaluation
* R², MAE and RMSE
* Scikit-learn Pipelines
* Saving models with Joblib
* Building Flask applications
* Creating REST APIs
* Backend input validation
* Data visualization
* Integrating ML with a web application
* Building a responsive frontend
* Writing automated tests

---

## 🤖 Machine Learning Workflow

The complete workflow is:

```text
Housing Dataset
      ↓
Data Preprocessing
      ↓
One-Hot Encoding
      ↓
Train/Test Split
      ↓
Linear Regression
      ↓
Random Forest Regressor
      ↓
Model Evaluation
      ↓
Best Model Selection
      ↓
Joblib Model Saving
      ↓
Flask Integration
      ↓
User Input
      ↓
House Price Prediction
```

---

## 📊 Dataset

The project contains **3,500 property records** covering 8 Pakistani cities:

* Islamabad
* Lahore
* Karachi
* Rawalpindi
* Peshawar
* Faisalabad
* Multan
* Gujranwala

### Features

| Feature     | Description                  |
| ----------- | ---------------------------- |
| `sqft`      | Property area in square feet |
| `bedrooms`  | Number of bedrooms           |
| `bathrooms` | Number of bathrooms          |
| `location`  | Property location            |
| `price`     | Target property price in PKR |

---

## 🧠 Models Used

Two regression models were trained and compared:

### 1. Linear Regression

Used as the baseline regression model.

### 2. Random Forest Regressor

A tree-based ensemble model used to capture more complex relationships between property features and price.

The best-performing model was automatically selected and saved.

---

## 🏆 Model Performance

The models were evaluated using an **80/20 train-test split**.

| Model                |   R² Score |                  MAE |                 RMSE |
| -------------------- | ---------: | -------------------: | -------------------: |
| **Random Forest** 🏆 | **0.9858** | **PKR 1,368,815.90** | **PKR 2,179,529.75** |
| Linear Regression    |     0.9400 |     PKR 2,847,212.01 |     PKR 4,483,444.72 |

### Best Model

**Random Forest Regressor**

**R² Score: 0.9858**

The Random Forest model was saved using Joblib and deployed in the Flask application.

> The reported performance is based on the synthetic dataset used for this educational project and should not be interpreted as real-world property-market accuracy.

---

## 🔄 Data Preprocessing

The project uses a Scikit-learn preprocessing pipeline.

### Numerical Features

* Square feet
* Bedrooms
* Bathrooms

These are processed using `StandardScaler`.

### Categorical Feature

`location`

is processed using:

```python
OneHotEncoder(handle_unknown="ignore")
```

The preprocessing and trained model are combined into a single Scikit-learn Pipeline.

This ensures that the exact same preprocessing is applied during prediction.

---

## 💾 Model Persistence

Instead of retraining the model every time the Flask application starts, the complete trained pipeline is saved using Joblib.

```text
models/
└── house_price_model.joblib
```

Flask loads the saved model and uses it directly for predictions.

---

## 🌐 Flask Web Application

The Machine Learning model is integrated into a Flask web application.

### Main Pages

* 🏠 Home
* 💰 Property Valuation
* ⚙️ How It Works
* 📊 Model Insights
* 📈 Market Trends
* 🔌 REST API
* ℹ️ About

The application provides a premium real-estate inspired responsive interface.

---

## 🔌 REST API

The project also exposes a prediction API.

### Endpoint

```text
POST /api/predict
```

### Example Request

```json
{
    "sqft": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "location": "Lahore"
}
```

### Example Response

```json
{
    "success": true,
    "predicted_price": 18500000,
    "currency": "PKR"
}
```

The API includes backend validation for:

* Missing fields
* Invalid values
* Negative values
* Unsupported locations
* Invalid property inputs

---

## 💰 PKR Price Formatting

Predicted property values are displayed using Pakistani currency formatting.

Examples:

```text
PKR 18,500,000
```

and:

```text
PKR 1.85 Crore
```

The application also supports Lacs-based formatting where appropriate.

---

## 📈 Data Visualization

The project includes visual analytics generated using Matplotlib and Seaborn.

Charts include:

* Model Comparison
* Price vs Square Feet
* Price by Location
* Price Distribution

These visualizations are available through the **Model Insights** and **Market Trends** sections.

---

## 🧪 Testing

Automated tests were implemented using Flask's testing utilities.

### Test Coverage

* Home route
* Insights route
* Prediction form
* API prediction
* Missing API fields
* Negative values
* Unsupported locations
* Currency formatting
* 404 handling

### Result

```text
10 tests passed
```

✅ All tests passed successfully.
<img width="1350" height="635" alt="house 1" src="https://github.com/user-attachments/assets/ccbb6bee-c636-4779-adee-2819425f82b7" />

---

## 🛠️ Tech Stack

```text
Python
Flask
Pandas
NumPy
Scikit-learn
Random Forest
Linear Regression
Joblib
Matplotlib
Seaborn
HTML5
CSS3
JavaScript
REST API
Jupyter Notebook
```

---

## 📁 Project Structure

```text
house-price-predictor/
│
├── app.py
├── train_model.py
├── test_app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── housing_data.csv
│
├── models/
│   ├── house_price_model.joblib
│   └── model_metadata.json
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── valuation.html
│   ├── result.html
│   ├── insights.html
│   ├── market_trends.html
│   ├── api.html
│   ├── about.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── charts/
│
└── notebooks/
    └── model_analysis.ipynb
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd house-price-predictor
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Train the Model

Run:

```bash
python train_model.py
```

This will:

1. Generate/load the dataset
2. Preprocess the data
3. Train the models
4. Evaluate model performance
5. Select the best model
6. Save the trained pipeline
7. Generate analytics charts
8. Save model metadata

---

## 🚀 Run the Application

Start Flask:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 💡 Future Improvements

Possible future improvements include:

* Real-world property datasets
* More advanced regression algorithms
* XGBoost / Gradient Boosting
* Hyperparameter optimization
* Property image analysis
* Map-based property selection
* Live real-estate market data
* User accounts and saved valuations
* Cloud deployment
* Advanced model explainability
* Property recommendation system

---

## 📚 Python Journey — Day 81

This project was an important milestone in my **Python Development Journey** because it brought together multiple concepts I have been learning throughout my **100 Days of Code** journey.

Instead of stopping at a Machine Learning model, I focused on turning the model into a complete application that users can actually interact with.

### Day 81 Focus:

**Machine Learning → Flask → REST API → Data Visualization → Full-Stack Integration**

---

## 🚀 Progress Continues

**Day 81 / 100 Days of Code 🐍**

Another project completed. Another step forward.

> **Keep building. Keep learning. Keep shipping. 🚀**

#Python #100DaysOfCode #MachineLearning #Flask #ScikitLearn #DataScience #PythonDevelopment #ArtificialIntelligence
