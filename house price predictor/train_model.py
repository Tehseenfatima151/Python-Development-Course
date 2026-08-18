import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for generating chart files
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error


DATA_DIR = "data"
MODELS_DIR = "models"
CHARTS_DIR = os.path.join("static", "images", "charts")
CSV_PATH = os.path.join(DATA_DIR, "housing_data.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "house_price_model.joblib")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")


def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)


def generate_synthetic_dataset(num_records=3500, random_seed=42):
    """
    Generate a realistic synthetic housing dataset tailored to the Pakistani real estate market.
    Locations and base price rates (PKR per sqft) reflect realistic urban housing dynamics.
    """
    np.random.seed(random_seed)

    locations = [
        "Islamabad",
        "Lahore",
        "Karachi",
        "Rawalpindi",
        "Peshawar",
        "Faisalabad",
        "Multan",
        "Gujranwala"
    ]

    # Approximate market baseline price per sqft in PKR
    location_base_rates = {
        "Islamabad": 11500,
        "Lahore": 9800,
        "Karachi": 9200,
        "Rawalpindi": 7200,
        "Peshawar": 6200,
        "Faisalabad": 5800,
        "Multan": 5200,
        "Gujranwala": 4800
    }

    records = []
    
    # Common house sizes in sqft (approx 3 Marla, 5 Marla, 7 Marla, 10 Marla, 1 Kanal, 2 Kanal)
    size_clusters = [
        (850, 200, 2, 2),    # ~3 Marla
        (1360, 250, 3, 3),   # ~5 Marla
        (1900, 300, 4, 3),   # ~7 Marla
        (2720, 400, 5, 4),   # ~10 Marla
        (4500, 600, 5, 5),   # ~1 Kanal
        (7500, 1000, 6, 6)   # ~2 Kanal
    ]

    for _ in range(num_records):
        loc = np.random.choice(locations, p=[0.20, 0.22, 0.18, 0.12, 0.08, 0.08, 0.06, 0.06])
        base_rate = location_base_rates[loc]

        # Select a cluster profile with some variance
        cluster_idx = np.random.choice(len(size_clusters), p=[0.15, 0.30, 0.22, 0.18, 0.10, 0.05])
        mean_sqft, std_sqft, default_bed, default_bath = size_clusters[cluster_idx]

        sqft = int(np.clip(np.random.normal(mean_sqft, std_sqft), 500, 9500))
        
        # Bedrooms & bathrooms tied to size with realistic jitter
        bedrooms = int(np.clip(default_bed + np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2]), 1, 8))
        bathrooms = int(np.clip(default_bath + np.random.choice([-1, 0, 1], p=[0.25, 0.55, 0.20]), 1, 8))

        # Realistic non-linear price valuation with market noise
        # 1. Base land & structure rate per sqft
        # 2. Premium for higher bedroom & bathroom count
        # 3. Non-linear scaling for luxury/larger plots
        # 4. Market noise (±7%)
        plot_efficiency = 1.0 + (sqft / 10000.0) * 0.15
        room_value = (bedrooms * 550000) + (bathrooms * 450000)
        base_valuation = (sqft * base_rate * plot_efficiency) + room_value
        
        noise_factor = np.random.normal(1.0, 0.06)
        price = int(np.round(base_valuation * noise_factor, -4))  # Round to nearest 10,000 PKR

        records.append({
            "sqft": sqft,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "location": loc,
            "price": price
        })

    df = pd.DataFrame(records)
    return df


def load_or_create_dataset():
    """Load dataset from disk or generate synthetic dataset."""
    ensure_directories()
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = generate_synthetic_dataset(num_records=3500)
        df.to_csv(CSV_PATH, index=False)
    return df


def create_charts(df, models_results, best_model_name):
    """Generate high-quality Matplotlib/Seaborn visualization charts."""
    # Set overall aesthetic style
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#cbd5e1'
    plt.rcParams['axes.linewidth'] = 0.8

    # 1. Model Comparison Chart
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    model_names = list(models_results.keys())
    r2_scores = [models_results[m]["r2"] for m in model_names]
    
    bar_colors = ['#3b82f6' if m != best_model_name else '#10b981' for m in model_names]
    bars = ax.bar(model_names, r2_scores, color=bar_colors, width=0.45, edgecolor='#0f172a', linewidth=1)
    
    ax.set_title("Model Performance Comparison (R² Score)", fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylabel("R² Score (Higher is Better)", fontsize=11, fontweight='600', color='#334155')
    ax.set_ylim(0, 1.05)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')
        
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "model_comparison.png"))
    plt.close(fig)

    # 2. Price vs Square Feet Scatter Plot
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sample_df = df.sample(n=min(1200, len(df)), random_state=42)
    
    palette = sns.color_palette("tab10", n_colors=len(df['location'].unique()))
    sns.scatterplot(
        data=sample_df,
        x='sqft',
        y=sample_df['price'] / 1e7,  # Price in Crores
        hue='location',
        alpha=0.65,
        palette=palette,
        s=45,
        ax=ax
    )
    
    ax.set_title("Property Price vs. Square Footage by Location", fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_xlabel("Area (Square Feet)", fontsize=11, fontweight='600', color='#334155')
    ax.set_ylabel("Price (PKR in Crores)", fontsize=11, fontweight='600', color='#334155')
    ax.legend(title="Location", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "price_vs_sqft.png"))
    plt.close(fig)

    # 3. Average Price by Location
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    avg_price_by_loc = df.groupby('location')['price'].mean().sort_values(ascending=False) / 1e7
    
    colors = sns.color_palette("crest", len(avg_price_by_loc))
    bars = ax.bar(avg_price_by_loc.index, avg_price_by_loc.values, color=colors, width=0.55, edgecolor='#0f172a', linewidth=0.8)
    
    ax.set_title("Average Property Value by City (in Crores PKR)", fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylabel("Average Price (Crores PKR)", fontsize=11, fontweight='600', color='#334155')
    ax.set_xlabel("City / Location", fontsize=11, fontweight='600', color='#334155')
    plt.xticks(rotation=25, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f} Cr',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1e293b')

    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "price_by_location.png"))
    plt.close(fig)

    # 4. Price Distribution Histogram & KDE
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.histplot(df['price'] / 1e7, kde=True, color='#0ea5e9', bins=35, ax=ax, edgecolor='white', linewidth=0.7)
    
    ax.set_title("Property Price Distribution", fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_xlabel("Price (PKR in Crores)", fontsize=11, fontweight='600', color='#334155')
    ax.set_ylabel("Number of Properties", fontsize=11, fontweight='600', color='#334155')
    
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "price_distribution.png"))
    plt.close(fig)


def train_and_evaluate():
    """Execute complete ML pipeline: data loading, preprocessing, model training, evaluation, and export."""
    ensure_directories()
    
    # 1. Load Dataset
    df = load_or_create_dataset()
    
    # Clean data (handle any nulls or invalid values)
    df = df.dropna()
    df = df[(df['sqft'] > 100) & (df['bedrooms'] > 0) & (df['bathrooms'] > 0) & (df['price'] > 0)]

    features = ['sqft', 'bedrooms', 'bathrooms', 'location']
    target = 'price'

    X = df[features]
    y = df[target]

    # 2. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # 3. Define Preprocessing Pipeline
    numerical_features = ['sqft', 'bedrooms', 'bathrooms']
    categorical_features = ['location']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )

    # 4. Define Candidate Models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=150,
            max_depth=16,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    }

    trained_pipelines = {}
    models_results = {}

    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        # Fit pipeline
        pipeline.fit(X_train, y_train)
        
        # Predictions
        y_pred = pipeline.predict(X_test)
        
        # Evaluate
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)

        models_results[name] = {
            "r2": float(r2),
            "mae": float(mae),
            "rmse": float(rmse)
        }
        trained_pipelines[name] = pipeline

    # 5. Automatically Select Best Model by R² score
    best_model_name = max(models_results, key=lambda k: models_results[k]["r2"])
    best_pipeline = trained_pipelines[best_model_name]

    # 6. Save Best Pipeline
    joblib.dump(best_pipeline, MODEL_PATH)

    # 7. Collect & Save Metadata
    available_locations = sorted(list(df['location'].unique()))
    metadata = {
        "dataset_records": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "features": features,
        "numerical_features": numerical_features,
        "categorical_features": categorical_features,
        "locations": available_locations,
        "best_model_name": best_model_name,
        "best_model_metrics": models_results[best_model_name],
        "models_comparison": models_results,
        "summary_stats": {
            "min_price": float(df['price'].min()),
            "max_price": float(df['price'].max()),
            "mean_price": float(df['price'].mean()),
            "median_price": float(df['price'].median()),
            "min_sqft": int(df['sqft'].min()),
            "max_sqft": int(df['sqft'].max()),
            "avg_sqft": float(df['sqft'].mean())
        }
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

    # 8. Generate Charts
    create_charts(df, models_results, best_model_name)

    # 9. Terminal Output as specified
    print("========================================")
    print("HOUSE PRICE MODEL TRAINING")
    print("========================================")
    print("")
    print("Dataset loaded successfully")
    print(f"Records: {len(df)}")
    print("")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print("")
    print("Model Performance")
    print("----------------------------------------")
    
    for name in ["Linear Regression", "Random Forest"]:
        res = models_results[name]
        print(name)
        print(f"R²   : {res['r2']:.4f}")
        print(f"MAE  : {res['mae']:,.2f} PKR")
        print(f"RMSE : {res['rmse']:,.2f} PKR")
        print("")

    print(f"Best Model: {best_model_name}")
    print("")
    print("Model saved successfully:")
    print(f"{MODEL_PATH}")
    print("========================================")

    return metadata


if __name__ == "__main__":
    train_and_evaluate()
