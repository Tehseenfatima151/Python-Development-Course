import os
import json
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "house-price-predictor-pakistan-ai-secret-2026")

# Directory and file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "house_price_model.joblib")
METADATA_PATH = os.path.join(BASE_DIR, "models", "model_metadata.json")

# Centralized model and metadata cache
MODEL_PIPELINE = None
MODEL_METADATA = None


def load_model_and_metadata():
    """Load model pipeline and metadata safely on startup."""
    global MODEL_PIPELINE, MODEL_METADATA
    
    # If model doesn't exist yet, trigger training
    if not os.path.exists(MODEL_PATH) or not os.path.exists(METADATA_PATH):
        try:
            from train_model import train_and_evaluate
            train_and_evaluate()
        except Exception as e:
            app.logger.error(f"Failed to auto-train model: {e}")

    if os.path.exists(MODEL_PATH):
        MODEL_PIPELINE = joblib.load(MODEL_PATH)
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            MODEL_METADATA = json.load(f)


# Load upon module initialization
load_model_and_metadata()


def format_currency_pkr(amount: float) -> str:
    """Format numeric value into standard comma-separated PKR representation."""
    return f"PKR {amount:,.0f}"


def format_pakistani_crore(amount: float) -> str:
    """
    Format numeric value in Pakistani financial denomination (Crore / Lacs).
    1 Crore = 10,000,000 (10 Million)
    1 Lac = 100,000 (100 Thousand)
    """
    if amount >= 10_000_000:
        crores = amount / 10_000_000
        return f"PKR {crores:.2f} Crore"
    elif amount >= 100_000:
        lacs = amount / 100_000
        return f"PKR {lacs:.2f} Lacs"
    else:
        return f"PKR {amount:,.0f}"


def validate_house_features(sqft, bedrooms, bathrooms, location):
    """
    Backend validation for housing inputs.
    Returns: (is_valid: bool, error_message: str or None, parsed_values: dict or None)
    """
    if MODEL_METADATA is None or 'locations' not in MODEL_METADATA:
        return False, "Model metadata not loaded. Please train the model.", None

    valid_locations = MODEL_METADATA.get("locations", [])

    # Validate square feet
    try:
        sqft_val = float(sqft)
        if sqft_val < 100 or sqft_val > 25000:
            return False, "Area must be between 100 sq ft and 25,000 sq ft.", None
    except (ValueError, TypeError):
        return False, "Invalid area entered. Please provide a numeric value.", None

    # Validate bedrooms
    try:
        bed_val = int(bedrooms)
        if bed_val < 1 or bed_val > 15:
            return False, "Bedrooms count must be between 1 and 15.", None
    except (ValueError, TypeError):
        return False, "Invalid bedrooms count entered.", None

    # Validate bathrooms
    try:
        bath_val = int(bathrooms)
        if bath_val < 1 or bath_val > 15:
            return False, "Bathrooms count must be between 1 and 15.", None
    except (ValueError, TypeError):
        return False, "Invalid bathrooms count entered.", None

    # Validate location
    if not location or str(location).strip() not in valid_locations:
        return False, f"Location '{location}' is unsupported. Allowed locations: {', '.join(valid_locations)}", None

    return True, None, {
        "sqft": sqft_val,
        "bedrooms": bed_val,
        "bathrooms": bath_val,
        "location": str(location).strip()
    }


def predict_price(sqft: float, bedrooms: int, bathrooms: int, location: str) -> float:
    """Execute prediction through the loaded scikit-learn pipeline."""
    if MODEL_PIPELINE is None:
        raise RuntimeError("ML Model pipeline is not loaded.")

    input_df = pd.DataFrame([{
        "sqft": sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "location": location
    }])

    predicted_val = MODEL_PIPELINE.predict(input_df)[0]
    return float(max(100_000, predicted_val))


@app.route("/", methods=["GET"])
def index():
    """Render Marketing / Product Landing Page."""
    locations = MODEL_METADATA.get("locations", []) if MODEL_METADATA else []
    best_model = MODEL_METADATA.get("best_model_name", "Random Forest") if MODEL_METADATA else "Random Forest"
    r2_score = MODEL_METADATA.get("best_model_metrics", {}).get("r2", 0.0) if MODEL_METADATA else 0.0
    mae = MODEL_METADATA.get("best_model_metrics", {}).get("mae", 0.0) if MODEL_METADATA else 0.0
    rmse = MODEL_METADATA.get("best_model_metrics", {}).get("rmse", 0.0) if MODEL_METADATA else 0.0
    dataset_records = MODEL_METADATA.get("dataset_records", 0) if MODEL_METADATA else 0

    return render_template(
        "index.html",
        locations=locations,
        best_model=best_model,
        r2_score=f"{r2_score:.2%}" if r2_score else "N/A",
        r2_raw=round(r2_score, 4),
        mae=format_currency_pkr(mae),
        rmse=format_currency_pkr(rmse),
        dataset_records=dataset_records
    )


@app.route("/valuation", methods=["GET"])
def valuation():
    """Render Dedicated AI Property Valuation Page."""
    locations = MODEL_METADATA.get("locations", []) if MODEL_METADATA else []
    best_model = MODEL_METADATA.get("best_model_name", "Random Forest") if MODEL_METADATA else "Random Forest"
    r2_score = MODEL_METADATA.get("best_model_metrics", {}).get("r2", 0.0) if MODEL_METADATA else 0.0
    dataset_records = MODEL_METADATA.get("dataset_records", 0) if MODEL_METADATA else 0

    return render_template(
        "valuation.html",
        locations=locations,
        best_model=best_model,
        r2_score=f"{r2_score:.2%}" if r2_score else "N/A",
        r2_raw=round(r2_score, 4),
        dataset_records=dataset_records,
        metadata=MODEL_METADATA or {}
    )


@app.route("/how-it-works", methods=["GET"])
def how_it_works():
    """Render Dedicated How It Works Page."""
    best_model = MODEL_METADATA.get("best_model_name", "Random Forest") if MODEL_METADATA else "Random Forest"
    r2_score = MODEL_METADATA.get("best_model_metrics", {}).get("r2", 0.0) if MODEL_METADATA else 0.0
    return render_template(
        "how_it_works.html",
        best_model=best_model,
        r2_score=f"{r2_score:.2%}" if r2_score else "N/A"
    )


@app.route("/insights", methods=["GET"])
def insights():
    """Render Model Insights and exploratory data analysis dashboard."""
    if MODEL_METADATA is None:
        load_model_and_metadata()

    return render_template("insights.html", metadata=MODEL_METADATA or {})


@app.route("/market-trends", methods=["GET"])
def market_trends():
    """Render Dedicated Market Trends Page."""
    if MODEL_METADATA is None:
        load_model_and_metadata()

    return render_template("market_trends.html", metadata=MODEL_METADATA or {})


@app.route("/api-docs", methods=["GET"])
@app.route("/api", methods=["GET"])
def api_docs():
    """Render Dedicated Developer REST API Documentation Page."""
    best_model = MODEL_METADATA.get("best_model_name", "Random Forest") if MODEL_METADATA else "Random Forest"
    r2_score = MODEL_METADATA.get("best_model_metrics", {}).get("r2", 0.0) if MODEL_METADATA else 0.0
    return render_template(
        "api_docs.html",
        best_model=best_model,
        r2_raw=round(r2_score, 4)
    )


@app.route("/about", methods=["GET"])
def about():
    """Render Dedicated About Page."""
    if MODEL_METADATA is None:
        load_model_and_metadata()

    return render_template("about.html", metadata=MODEL_METADATA or {})


@app.route("/predict", methods=["POST"])
def predict_form():
    """Handle standard HTML form submission."""
    sqft = request.form.get("sqft")
    bedrooms = request.form.get("bedrooms")
    bathrooms = request.form.get("bathrooms")
    location = request.form.get("location")

    is_valid, err_msg, parsed = validate_house_features(sqft, bedrooms, bathrooms, location)
    if not is_valid:
        flash(err_msg, "danger")
        return redirect(url_for("valuation"))

    try:
        raw_price = predict_price(
            parsed["sqft"],
            parsed["bedrooms"],
            parsed["bathrooms"],
            parsed["location"]
        )

        formatted_pkr = format_currency_pkr(raw_price)
        formatted_crore = format_pakistani_crore(raw_price)
        price_per_sqft = raw_price / parsed["sqft"]

        model_info = {
            "name": MODEL_METADATA.get("best_model_name", "Random Forest Regressor") if MODEL_METADATA else "ML Model",
            "r2_score": MODEL_METADATA.get("best_model_metrics", {}).get("r2", 0.0) if MODEL_METADATA else 0.0,
            "mae": MODEL_METADATA.get("best_model_metrics", {}).get("mae", 0.0) if MODEL_METADATA else 0.0,
            "rmse": MODEL_METADATA.get("best_model_metrics", {}).get("rmse", 0.0) if MODEL_METADATA else 0.0,
        }

        return render_template(
            "result.html",
            property_input=parsed,
            predicted_price_raw=raw_price,
            formatted_pkr=formatted_pkr,
            formatted_crore=formatted_crore,
            price_per_sqft=format_currency_pkr(price_per_sqft),
            model_info=model_info
        )
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        flash("An error occurred while calculating the property valuation. Please try again.", "danger")
        return redirect(url_for("valuation"))


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    REST API endpoint for property price valuation.
    Expects JSON: { "sqft": 1800, "bedrooms": 3, "bathrooms": 2, "location": "Lahore" }
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON with Content-Type: application/json."
        }), 400

    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Empty JSON payload provided."
        }), 400

    sqft = data.get("sqft")
    bedrooms = data.get("bedrooms")
    bathrooms = data.get("bathrooms")
    location = data.get("location")

    # Backend validation
    is_valid, err_msg, parsed = validate_house_features(sqft, bedrooms, bathrooms, location)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": err_msg
        }), 400

    try:
        price = predict_price(
            parsed["sqft"],
            parsed["bedrooms"],
            parsed["bathrooms"],
            parsed["location"]
        )

        return jsonify({
            "success": True,
            "predicted_price": round(price, 2),
            "formatted_price": format_currency_pkr(price),
            "formatted_crore": format_pakistani_crore(price),
            "currency": "PKR",
            "price_per_sqft": round(price / parsed["sqft"], 2),
            "model": MODEL_METADATA.get("best_model_name", "Random Forest") if MODEL_METADATA else "Random Forest",
            "r2_score": MODEL_METADATA.get("best_model_metrics", {}).get("r2") if MODEL_METADATA else None,
            "input": parsed
        }), 200

    except Exception as e:
        app.logger.error(f"API prediction error: {e}")
        return jsonify({
            "success": False,
            "error": "Internal prediction calculation error occurred."
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "API route not found."}), 404
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Internal server error occurred."}), 500
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
