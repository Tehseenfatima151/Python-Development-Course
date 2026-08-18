# AI-Powered House Price Predictor (Pakistan - PKR) 🏡🤖

A production-grade, portfolio-ready Machine Learning web application and REST API designed to provide instant property valuations across major Pakistani real estate markets (Lahore, Islamabad, Karachi, Rawalpindi, Peshawar, Faisalabad, Multan, and Gujranwala).

Built with **Python, Flask, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, and a modern responsive UI**.

---

## 🌟 Key Features

- **End-to-End Scikit-Learn Pipeline**: Integrated preprocessing (`ColumnTransformer`, `StandardScaler`, and `OneHotEncoder`) serialized with `joblib` for identical transformations during inference and training.
- **Empirical Multi-Model Benchmarking**: Trains and compares **Linear Regression** and **Random Forest Regressor** on an 80/20 train-test split, automatically selecting and deploying the superior model ($R^2 \approx 0.9858$).
- **Pakistani Market Calibration (PKR)**: Native support for Pakistani property metrics, including square footage, Marla / Kanal conversions, and dual denomination formatting (**PKR 18,500,000** & **PKR 1.85 Crore**).
- **Interactive Modern UI**: Built with a luxury dark glassmorphic SaaS aesthetic, ambient background lighting, quick-select Marla presets, and responsive layout across mobile and desktop.
- **Instant REST API (`POST /api/predict`)**: Production-ready endpoint with backend payload validation, precise error codes, and JSON responses.
- **Model Insights Dashboard**: Transparent data science portal showcasing live performance metrics ($R^2$, MAE, RMSE), sample volumes, and embedded analytical visualizations.

---

## 🛠️ Tech Stack

| Domain | Technologies & Libraries |
|---|---|
| **Backend & Web Framework** | Python 3.14+, Flask 3.0+ |
| **Machine Learning** | Scikit-Learn, Joblib, NumPy |
| **Data Processing & Analytics** | Pandas, Matplotlib, Seaborn |
| **Frontend UI/UX** | HTML5, Modern CSS (Glassmorphism), JavaScript (ES6+), FontAwesome |
| **Data Science Exploration** | Jupyter Notebook (`model_analysis.ipynb`) |

---

## 📊 Dataset & Model Performance

### Dataset Information
- **Location**: `data/housing_data.csv`
- **Volume**: 3,500 records
- **Features**: `sqft` (Covered Area), `bedrooms`, `bathrooms`, `location` (City)
- **Target**: `price` (Valuation in Pakistani Rupees - PKR)
- **Covered Cities**: Islamabad, Lahore, Karachi, Rawalpindi, Peshawar, Faisalabad, Multan, Gujranwala.

> **Note on Dataset**: The dataset in `data/housing_data.csv` was programmatically generated to model realistic Pakistani urban property pricing dynamics (including city-tier premiums and non-linear land/construction scaling) for educational, demonstration, and portfolio benchmarking purposes.

### Model Benchmark Results (80% Train / 20% Test Split)

| Model Architecture | $R^2$ Score (Accuracy) | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Status |
|---|---|---|---|---|
| **Random Forest Regressor** | **0.9858** | **PKR 1,368,815.90** | **PKR 2,179,529.75** | 🏆 **Deployed Pipeline** |
| **Linear Regression** | 0.9400 | PKR 2,847,212.01 | PKR 4,483,444.72 | Baseline Candidate |

*The model with the highest $R^2$ score is automatically selected and saved to `models/house_price_model.joblib`.*

---

## 🔄 Machine Learning Workflow

```text
       CSV Dataset (data/housing_data.csv)
                      ↓
  Data Cleaning & Train/Test Split (80/20)
                      ↓
  ColumnTransformer (StandardScaler + OneHotEncoder)
                      ↓
  Multi-Model Training (Linear Regression & Random Forest)
                      ↓
  Model Evaluation (R², MAE, RMSE)
                      ↓
  Automated Selection of Best Model
                      ↓
  Model Pipeline Export (models/house_price_model.joblib)
                      ↓
  Flask Web App & REST API (Loads Pipeline Once into Memory)
```

---

## 📁 Project Structure

```text
house-price-predictor/
│
├── app.py                      # Flask application (Routes, API, Validation, Formatting)
├── train_model.py              # ML Pipeline training, benchmarking, chart generation & serialization
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── housing_data.csv        # Housing dataset (3,500 records)
│
├── models/
│   ├── house_price_model.joblib # Serialized Scikit-Learn Pipeline
│   └── model_metadata.json     # Saved metrics, features, and locations
│
├── templates/
│   ├── base.html               # Master layout with navigation & footer
│   ├── index.html              # Landing page, hero, valuation form & API docs
│   ├── result.html             # Valuation result view with specifications breakdown
│   ├── insights.html           # Model insights, performance table & charts
│   ├── 404.html                # Custom 404 Not Found page
│   └── 500.html                # Custom 500 Internal Server Error page
│
├── static/
│   ├── css/
│   │   └── style.css           # Premium real estate & AI glassmorphic styling
│   ├── js/
│   │   └── script.js           # Marla presets, form validation & instant AJAX valuation
│   └── images/
│       └── charts/             # Generated Matplotlib/Seaborn analytics plots
│           ├── model_comparison.png
│           ├── price_vs_sqft.png
│           ├── price_by_location.png
│           └── price_distribution.png
│
└── notebooks/
    └── model_analysis.ipynb    # Jupyter Notebook for EDA & model experimentation
```

---

## 🚀 Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/house-price-predictor.git
cd house-price-predictor
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the ML Model & Generate Visualizations
```bash
python train_model.py
```

*Terminal Output:*
```text
========================================
HOUSE PRICE MODEL TRAINING
========================================

Dataset loaded successfully
Records: 3500

Training samples: 2800
Testing samples: 700

Model Performance
----------------------------------------
Linear Regression
R²   : 0.9400
MAE  : 2,847,212.01 PKR
RMSE : 4,483,444.72 PKR

Random Forest
R²   : 0.9858
MAE  : 1,368,815.90 PKR
RMSE : 2,179,529.75 PKR

Best Model: Random Forest

Model saved successfully:
models/house_price_model.joblib
========================================
```

### 5. Launch the Flask Application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🌐 API Documentation

### Predict House Price Endpoint

- **Endpoint**: `/api/predict`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`

#### Request Payload
```json
{
  "sqft": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "Lahore"
}
```

#### Successful Response (`200 OK`)
```json
{
  "currency": "PKR",
  "formatted_crore": "PKR 1.85 Crore",
  "formatted_price": "PKR 18,500,000",
  "input": {
    "bathrooms": 2,
    "bedrooms": 3,
    "location": "Lahore",
    "sqft": 1800.0
  },
  "model": "Random Forest",
  "predicted_price": 18500000.0,
  "price_per_sqft": 10277.78,
  "r2_score": 0.9858164442791897,
  "success": true
}
```

#### Error Response (`400 Bad Request`)
```json
{
  "error": "Location 'UnknownCity' is unsupported. Allowed locations: Faisalabad, Gujranwala, Islamabad, Karachi, Lahore, Multan, Peshawar, Rawalpindi",
  "success": false
}
```

#### cURL Example
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sqft": 1800, "bedrooms": 3, "bathrooms": 2, "location": "Lahore"}'
```

---

## 📸 Application Preview

*(Screenshots can be added here upon deployment)*
- **Landing Page & Valuation Form**: Modern dark SaaS theme with real-time Marla converter.
- **Valuation Result Screen**: Price breakdown, price/sqft metric, and model confidence stats.
- **Model Insights Dashboard**: Multi-model comparison table and generated visual diagnostics.

---

## 🔮 Future Enhancements

- [ ] Add historical price trend analysis and time-series forecasting.
- [ ] Incorporate additional property features (e.g., plot vs. built house, floor number, year built).
- [ ] Add interactive Leaflet/Mapbox maps displaying neighborhood price heatmaps.
- [ ] Containerize application with Docker & deploy to AWS / Render / Hugging Face Spaces.

---

## 📄 License

This project is licensed under the MIT License - feel free to use it for educational and portfolio purposes.
