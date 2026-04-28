from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Portfolio Analysis ---
class Asset(BaseModel):
    ticker: str
    weight: float  # portfolio weight between 0 and 1
    expected_return: float
    volatility: float

class PortfolioRequest(BaseModel):
    assets: List[Asset]
    risk_free_rate: float = 0.02  # default 2% risk-free rate

class PortfolioResponse(BaseModel):
    expected_return: float
    volatility: float
    sharpe_ratio: float
    risk_level: str  # low, medium, high

# --- Risk Scoring ---
class ClientProfile(BaseModel):
    client_id: str
    age: int
    income: float
    debt: float
    credit_score: int
    employment_years: float
    previous_defaults: int

class RiskResponse(BaseModel):
    client_id: str
    risk_score: float
    risk_category: str  # low, medium, high

# --- Transaction Lookup ---
class TransactionQuery(BaseModel):
    client_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Transaction(BaseModel):
    id: int
    client_id: str
    amount: float
    merchant: str
    timestamp: datetime
    flagged: bool

# --- Fraud Detection ---
class TransactionInput(BaseModel):
    client_id: str
    amount: float
    merchant: str
    hour_of_day: int
    is_foreign: bool
    previous_fraud_count: int

class FraudResponse(BaseModel):
    client_id: str
    is_fraudulent: bool
    confidence: float
    reason: str

# --- Market Sentiment ---
class SentimentRequest(BaseModel):
    ticker: str
    text: str  # news headline or company description

class SentimentResponse(BaseModel):
    ticker: str
    sentiment: str  # positive, negative, neutral
    confidence: float