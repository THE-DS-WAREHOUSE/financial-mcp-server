from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime
from databases import Database
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)

# --- Clients table ---
# Stores client financial profiles used for risk scoring
clients = Table(
    "clients",
    metadata,
    Column("id", String, primary_key=True),
    Column("age", Integer, nullable=False),
    Column("income", Float, nullable=False),
    Column("debt", Float, nullable=False),
    Column("credit_score", Integer, nullable=False),
    Column("employment_years", Float, nullable=False),
    Column("previous_defaults", Integer, nullable=False),
)

# --- Transactions table ---
# Stores all client transactions for lookup and fraud detection
transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_id", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("merchant", String, nullable=False),
    Column("timestamp", DateTime, default=datetime.utcnow),
    Column("flagged", Boolean, default=False),
)

# --- Portfolios table ---
# Stores portfolio analysis results per client
portfolios = Table(
    "portfolios",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_id", String, nullable=False),
    Column("expected_return", Float, nullable=False),
    Column("volatility", Float, nullable=False),
    Column("sharpe_ratio", Float, nullable=False),
    Column("risk_level", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
)