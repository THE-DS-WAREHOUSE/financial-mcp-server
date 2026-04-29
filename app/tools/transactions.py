import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import TransactionQuery, Transaction
from db import database, transactions
from datetime import datetime

async def get_transactions(query: TransactionQuery) -> list:

    # Start with base query selecting all transactions
    sql = transactions.select()

    # Filter by client_id if provided
    if query.client_id:
        sql = sql.where(transactions.c.client_id == query.client_id)

    # Filter by start date if provided
    if query.start_date:
        sql = sql.where(transactions.c.timestamp >= query.start_date)

    # Filter by end date if provided
    if query.end_date:
        sql = sql.where(transactions.c.timestamp <= query.end_date)

    # Order by most recent first
    sql = sql.order_by(transactions.c.timestamp.desc())

    results = await database.fetch_all(sql)

    # Convert each row to a Transaction schema object
    return [
        Transaction(
            id=row["id"],
            client_id=row["client_id"],
            amount=row["amount"],
            merchant=row["merchant"],
            timestamp=row["timestamp"],
            flagged=row["flagged"]
        )
        for row in results
    ]

async def insert_transaction(
    client_id: str,
    amount: float,
    merchant: str,
    flagged: bool = False
) -> int:
    # Inserts a new transaction into PostgreSQL
    # Returns the ID of the newly created record
    query = transactions.insert().values(
        client_id=client_id,
        amount=amount,
        merchant=merchant,
        timestamp=datetime.utcnow(),
        flagged=flagged
    )
    return await database.execute(query)