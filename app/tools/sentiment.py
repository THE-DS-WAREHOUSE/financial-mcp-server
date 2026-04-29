import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformers import pipeline
from schemas import SentimentRequest, SentimentResponse

# Load FinBERT once at module startup
# Reusing the same model from financial-sentiment-service
# ProsusAI/finbert is free, runs locally, no API key needed
sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    top_k=1
)

def analyze_sentiment(request: SentimentRequest) -> SentimentResponse:

    # Run the text through FinBERT
    result = sentiment_pipeline(request.text)[0][0]

    return SentimentResponse(
        ticker=request.ticker,
        sentiment=result["label"],
        confidence=round(result["score"], 4)
    )