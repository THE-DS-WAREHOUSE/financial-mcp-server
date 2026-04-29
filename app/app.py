import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from db import database, metadata, engine
from schemas import (
    PortfolioRequest, ClientProfile, TransactionQuery,
    TransactionInput, SentimentRequest
)
from tools.portfolio import analyze_portfolio
from tools.risk_scoring import score_client
from tools.fraud import detect_fraud
from tools.sentiment import analyze_sentiment
from tools.transactions import get_transactions, insert_transaction

# --- Initialize MCP server ---
# FastMCP wraps your tools and exposes them to Claude Desktop
# The name appears in Claude Desktop's connected tools list
mcp = FastMCP("Financial MCP Server")

# --- Connect and disconnect database on startup/shutdown ---
@asynccontextmanager
async def lifespan():
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

# --- Tool 1: Portfolio Analysis ---
# Claude can call this to analyze a portfolio of assets
@mcp.tool()
def portfolio_analysis(request: PortfolioRequest) -> dict:
    """Analyze a portfolio of assets and return expected return, volatility and Sharpe ratio."""
    result = analyze_portfolio(request)
    return result.dict()

# --- Tool 2: Risk Scoring ---
# Claude can call this to score a client's credit risk
@mcp.tool()
def risk_scoring(profile: ClientProfile) -> dict:
    """Score a client's financial risk profile using XGBoost. Returns risk score and category."""
    result = score_client(profile)
    return result.dict()

# --- Tool 3: Transaction Lookup ---
# Claude can call this to retrieve transaction history from PostgreSQL
@mcp.tool()
async def transaction_lookup(query: TransactionQuery) -> list:
    """Look up transaction history for a client from the database. Filter by client ID or date range."""
    results = await get_transactions(query)
    return [r.dict() for r in results]

# --- Tool 4: Fraud Detection ---
# Claude can call this to flag a transaction as fraudulent or clean
@mcp.tool()
def fraud_detection(transaction: TransactionInput) -> dict:
    """Detect whether a transaction is fraudulent using XGBoost. Returns fraud flag and confidence score."""
    result = detect_fraud(transaction)
    return result.dict()

# --- Tool 5: Market Sentiment ---
# Claude can call this to analyze sentiment of financial news using FinBERT
@mcp.tool()
def market_sentiment(request: SentimentRequest) -> dict:
    """Analyze market sentiment for a stock ticker using FinBERT. Returns positive, negative, or neutral."""
    result = analyze_sentiment(request)
    return result.dict()

if __name__ == "__main__":
    mcp.run()