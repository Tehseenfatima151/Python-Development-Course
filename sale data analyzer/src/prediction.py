"""Sales forecasting module using Simple Linear Regression."""

import logging
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import config
from src import analysis

logger = logging.getLogger("sales_analyzer.prediction")

PREDICTION_DISCLAIMER = (
    "This prediction is based on a simple linear regression model and should be "
    "treated as a basic trend estimate rather than a production-grade forecasting model."
)


def predict_next_month_sales(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Train a Simple Linear Regression model on aggregated monthly sales data
    and forecast sales for the next sequential month.
    """
    monthly_df = analysis.get_monthly_sales(df)
    n_observations = len(monthly_df)

    if n_observations < config.MIN_OBSERVATIONS_FOR_REGRESSION:
        logger.warning(
            f"Insufficient monthly observations ({n_observations}) for linear regression. "
            f"Minimum required: {config.MIN_OBSERVATIONS_FOR_REGRESSION}"
        )
        return {
            "is_valid": False,
            "error_message": (
                f"Insufficient historical data: Found {n_observations} monthly data point(s). "
                f"At least {config.MIN_OBSERVATIONS_FOR_REGRESSION} consecutive months are required for regression."
            ),
            "predicted_sales": 0.0,
            "r2_score": 0.0,
            "slope": 0.0,
            "intercept": 0.0,
            "n_observations": n_observations,
            "next_period_label": "N/A",
            "model_description": "Simple Linear Regression (Unfitted - Insufficient Data)",
            "disclaimer": PREDICTION_DISCLAIMER,
        }

    # Features: Sequential Month Index (1, 2, ..., N)
    X = np.arange(1, n_observations + 1).reshape(-1, 1)
    y = monthly_df["Sales"].values

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Calculate model metrics
    y_pred_train = model.predict(X)
    r2 = float(r2_score(y, y_pred_train))
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)

    # Predict Next Month (N + 1)
    next_month_idx = np.array([[n_observations + 1]])
    predicted_raw = float(model.predict(next_month_idx)[0])
    predicted_sales = max(0.0, predicted_raw)  # Sales cannot be negative

    # Determine next month label
    last_ym_str = monthly_df["Year_Month"].iloc[-1]
    try:
        last_period = pd.Period(last_ym_str, freq="M")
        next_period = last_period + 1
        next_period_label = str(next_period)
    except Exception:
        next_period_label = f"Month {n_observations + 1}"

    logger.info(
        f"Linear Regression trained on {n_observations} months. "
        f"Slope: {slope:.2f}, Intercept: {intercept:.2f}, R2: {r2:.3f}. "
        f"Forecast for {next_period_label}: ${predicted_sales:,.2f}"
    )

    return {
        "is_valid": True,
        "predicted_sales": round(predicted_sales, 2),
        "r2_score": round(r2, 4),
        "slope": round(slope, 2),
        "intercept": round(intercept, 2),
        "n_observations": n_observations,
        "next_period_label": next_period_label,
        "model_description": "Simple Linear Regression (Ordinary Least Squares)",
        "disclaimer": PREDICTION_DISCLAIMER,
        "equation": f"Sales = ({slope:.2f} * Month_Index) + {intercept:.2f}",
    }
