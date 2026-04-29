import numpy as np
import xgboost as xgb
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import ClientProfile, RiskResponse

# --- Train a simple XGBoost risk scoring model ---
# In production this would be loaded from MLflow or a model registry
# Here we train on synthetic data that mirrors real credit risk patterns
def train_risk_model():
    # Synthetic training data — mimics real credit risk profiles
    # Features: age, income, debt, credit_score, employment_years, previous_defaults
    X_train = np.array([
        # low risk profiles
        [45, 85000, 10000, 750, 15, 0],
        [38, 95000, 5000,  780, 12, 0],
        [52, 120000, 8000, 800, 20, 0],
        [41, 75000, 12000, 720, 10, 0],
        [35, 60000, 7000,  710, 8,  0],
        # medium risk profiles
        [29, 40000, 15000, 640, 3,  1],
        [33, 45000, 20000, 620, 5,  1],
        [27, 35000, 18000, 600, 2,  1],
        [31, 42000, 22000, 610, 4,  1],
        [36, 48000, 25000, 630, 6,  1],
        # high risk profiles
        [23, 20000, 18000, 520, 1,  3],
        [25, 22000, 20000, 510, 0,  4],
        [22, 18000, 17000, 490, 1,  5],
        [24, 21000, 19000, 500, 0,  3],
        [26, 23000, 21000, 480, 1,  4],
    ])

    # Labels: 0 = low risk, 1 = medium risk, 2 = high risk
    y_train = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2])

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

# Train model once at module load time
# Avoids retraining on every request
risk_model = train_risk_model()

def score_client(profile: ClientProfile) -> RiskResponse:

    # Build feature vector in the same order as training data
    features = np.array([[
        profile.age,
        profile.income,
        profile.debt,
        profile.credit_score,
        profile.employment_years,
        profile.previous_defaults
    ]])

    # Get predicted class and probability
    predicted_class = int(risk_model.predict(features)[0])
    probabilities = risk_model.predict_proba(features)[0]
    risk_score = round(float(probabilities[predicted_class]), 4)

    # Map predicted class to human readable category
    category_map = {0: "low", 1: "medium", 2: "high"}
    risk_category = category_map[predicted_class]

    return RiskResponse(
        client_id=profile.client_id,
        risk_score=risk_score,
        risk_category=risk_category
    )