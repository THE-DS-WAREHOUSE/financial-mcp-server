# financial-mcp-server

A production-grade Financial MCP Server exposing five AI-powered tools — portfolio analysis (Sharpe ratio, volatility), XGBoost credit risk scoring, XGBoost fraud detection, transaction lookup, and FinBERT market sentiment analysis — directly connectable from Claude Desktop or any LangGraph agent via the Model Context Protocol (MCP).

---

## Project Structure

```
financial-mcp-server/
├── app/
│   ├── tools/
│   │   ├── portfolio.py        # Portfolio analysis — Sharpe ratio, volatility, expected return
│   │   ├── risk_scoring.py     # XGBoost credit risk scoring — low / medium / high
│   │   ├── fraud.py            # XGBoost fraud detection — clean / fraudulent + confidence
│   │   ├── transactions.py     # PostgreSQL transaction lookup and insertion
│   │   └── sentiment.py        # FinBERT market sentiment — positive / negative / neutral
│   ├── app.py                  # FastMCP server — registers all 5 tools
│   ├── db.py                   # PostgreSQL connection and table definitions
│   └── schemas.py              # Pydantic input/output schemas for all tools
├── Dockerfile                  # Containerizes the MCP server
├── docker-compose.yml          # Orchestrates MCP server + PostgreSQL
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (not committed)
```

---

## Features

- **5 production-grade MCP tools** callable directly from Claude Desktop or any MCP-compatible agent
- **XGBoost credit risk scoring** — classifies clients as low, medium, or high risk
- **XGBoost fraud detection** — flags transactions as clean or fraudulent with confidence score
- **Portfolio analysis** — calculates expected return, volatility, and Sharpe ratio
- **FinBERT market sentiment** — classifies financial text as positive, negative, or neutral
- **Transaction lookup** — queries PostgreSQL by client ID or date range
- **Fully containerized** with Docker Compose — MCP server + PostgreSQL

---

## Tech Stack

- `MCP` (Model Context Protocol) — Anthropic's open protocol for tool calling
- `FastMCP` — Python MCP server SDK
- `XGBoost` — credit risk and fraud detection models
- `FinBERT` (ProsusAI/finbert) — financial NLP sentiment model
- `PostgreSQL` — transaction storage
- `Pydantic` — input/output validation
- `Docker Compose` — containerization

---

## MCP Tools

### Tool 1: `portfolio_analysis`
Analyzes a portfolio of assets and returns expected return, volatility, and Sharpe ratio.

**Input:**
```json
{
  "assets": [
    {"ticker": "AAPL", "weight": 0.6, "expected_return": 0.12, "volatility": 0.18},
    {"ticker": "GOOGL", "weight": 0.4, "expected_return": 0.10, "volatility": 0.15}
  ],
  "risk_free_rate": 0.02
}
```

**Output:**
```json
{
  "expected_return": 0.112,
  "volatility": 0.121,
  "sharpe_ratio": 0.76,
  "risk_level": "medium"
}
```

---

### Tool 2: `risk_scoring`
Scores a client's credit risk using XGBoost. Returns a risk score and category.

**Input:**
```json
{
  "client_id": "C001",
  "age": 25,
  "income": 22000,
  "debt": 19000,
  "credit_score": 500,
  "employment_years": 1,
  "previous_defaults": 4
}
```

**Output:**
```json
{
  "client_id": "C001",
  "risk_score": 0.8926,
  "risk_category": "high"
}
```

---

### Tool 3: `transaction_lookup`
Retrieves transaction history from PostgreSQL filtered by client ID or date range.

**Input:**
```json
{
  "client_id": "C001",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T00:00:00"
}
```

---

### Tool 4: `fraud_detection`
Detects whether a transaction is fraudulent using XGBoost. Returns a fraud flag, confidence score, and human-readable reason.

**Input:**
```json
{
  "client_id": "C001",
  "amount": 8000,
  "merchant": "Unknown Merchant",
  "hour_of_day": 3,
  "is_foreign": true,
  "previous_fraud_count": 3
}
```

**Output:**
```json
{
  "client_id": "C001",
  "is_fraudulent": true,
  "confidence": 0.97,
  "reason": "unusually high amount, transaction at unusual hour, foreign transaction, multiple previous fraud flags"
}
```

---

### Tool 5: `market_sentiment`
Analyzes market sentiment of financial text using FinBERT. Returns positive, negative, or neutral with confidence score.

**Input:**
```json
{
  "ticker": "AAPL",
  "text": "The company reported strong earnings growth and raised its revenue guidance for next quarter"
}
```

**Output:**
```json
{
  "ticker": "AAPL",
  "sentiment": "positive",
  "confidence": 0.954
}
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/financial-mcp-server.git
cd financial-mcp-server
```

### 2. Configure environment variables

Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/financial_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db
```

### 3. Run with Docker
```bash
docker compose up --build
```

### 4. Or run locally
```bash
pip install -r requirements.txt
cd app
python app.py
```

---

## Connect to Claude Desktop

Add this to your `claude_desktop_config.json`:

**Windows path:**
```
C:\Users\<your-username>\AppData\Roaming\Claude\claude_desktop_config.json
```

**Config:**
```json
{
  "mcpServers": {
    "financial-mcp-server": {
      "command": "C:\\path\\to\\financial-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\financial-mcp-server\\app\\app.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\financial-mcp-server\\app"
      }
    }
  }
}
```

Restart Claude Desktop and the tools will appear under **Conectores → financial-mcp-server**.

---

## Docker Commands

| Command                     | Description                                      |
|-----------------------------|--------------------------------------------------|
| `docker compose up --build` | Build images and start containers                |
| `docker compose up`         | Start without rebuilding                         |
| `docker compose stop`       | Pause containers                                 |
| `docker compose down`       | Stop and remove containers                       |
| `docker compose down -v`    | Stop, remove containers and delete DB volume     |
| `docker compose logs api`   | View MCP server logs                             |

---

## Requirements

```
fastapi
uvicorn
mcp[cli]
sqlalchemy
databases
asyncpg
psycopg2-binary
python-dotenv
xgboost
scikit-learn
numpy
pandas
transformers
torch
```

---

## Notes

- XGBoost models are trained on synthetic data at startup — in production these would be loaded from MLflow or a model registry
- FinBERT runs locally inside the container, no external API key needed
- PostgreSQL data persists via a named Docker volume across container restarts
- The `.env` file should never be committed — add it to `.gitignore`
- When running in Docker, Claude Desktop cannot connect directly — use the local setup for Claude Desktop integration
