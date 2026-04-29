import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import xgboost as xgb
from schemas import TransactionInput, FraudResponse

# --- Train a simple XGBoost fraud detection model ---
# Features: amount, hour_of_day, is_foreign, previous_fraud_count
def train_fraud_model():
    # Synthetic training data mimicking real transaction fraud patterns
    # Features: amount, hour_of_day, is_foreign, previous_fraud_count
    X_train = np.array([
        # clean transactions
        [50,   9,  0, 0],
        [120,  14, 0, 0],
        [200,  11, 0, 0],
        [80,   16, 0, 0],
        [350,  10, 0, 0],
        [500,  13, 1, 0],
        [150,  15, 1, 0],
        [900,  12, 1, 0],
        # fraudulent transactions
        [4500, 2,  1, 2],
        [8000, 3,  1, 3],
        [3200, 1,  1, 4],
        [6000, 23, 1, 2],
        [7500, 4,  1, 5],
        [5000, 2,  1, 3],
        [9000, 3,  1, 4],
    ])

    # Labels: 0 = clean, 1 = fraudulent
    y_train = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1])

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

# Train model once at module load time
fraud_model = train_fraud_model()

def detect_fraud(transaction: TransactionInput) -> FraudResponse:

    features = np.array([[
        transaction.amount,
        transaction.hour_of_day,
        int(transaction.is_foreign),
        transaction.previous_fraud_count
    ]])

    predicted_class = int(fraud_model.predict(features)[0])
    probabilities = fraud_model.predict_proba(features)[0]
    confidence = round(float(probabilities[predicted_class]), 4)
    is_fraudulent = predicted_class == 1

    # Build a human readable reason based on the transaction features
    reasons = []
    if transaction.amount > 3000:
        reasons.append("unusually high amount")
    if transaction.hour_of_day in range(0, 5):
        reasons.append("transaction at unusual hour")
    if transaction.is_foreign:
        reasons.append("foreign transaction")
    if transaction.previous_fraud_count > 1:
        reasons.append("multiple previous fraud flags")

    reason = ", ".join(reasons) if reasons else "no suspicious indicators"

    return FraudResponse(
        client_id=transaction.client_id,
        is_fraudulent=is_fraudulent,
        confidence=confidence,
        reason=reason
    )