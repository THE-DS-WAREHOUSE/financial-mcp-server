import numpy as np
from schemas import PortfolioRequest, PortfolioResponse

def analyze_portfolio(request: PortfolioRequest) -> PortfolioResponse:

    # Extract weights and returns from the request
    weights = np.array([asset.weight for asset in request.assets])
    returns = np.array([asset.expected_return for asset in request.assets])
    volatilities = np.array([asset.volatility for asset in request.assets])

    # Normalize weights to ensure they sum to 1
    # This handles cases where the user provides weights that don't add up perfectly
    weights = weights / weights.sum()

    # --- Expected Portfolio Return ---
    # Weighted average of individual asset returns
    portfolio_return = float(np.dot(weights, returns))

    # --- Portfolio Volatility ---
    # Simplified calculation assuming no correlation between assets
    # In production you'd use a full covariance matrix
    # Formula: sqrt(sum of (weight_i^2 * volatility_i^2))
    portfolio_volatility = float(np.sqrt(np.dot(weights ** 2, volatilities ** 2)))

    # --- Sharpe Ratio ---
    # Measures return per unit of risk taken
    # Formula: (portfolio_return - risk_free_rate) / portfolio_volatility
    # Higher is better — above 1.0 is generally considered good
    if portfolio_volatility == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = round(
            (portfolio_return - request.risk_free_rate) / portfolio_volatility, 4
        )

    # --- Risk Level Classification ---
    # Based on portfolio volatility thresholds
    if portfolio_volatility < 0.10:
        risk_level = "low"
    elif portfolio_volatility < 0.20:
        risk_level = "medium"
    else:
        risk_level = "high"

    return PortfolioResponse(
        expected_return=round(portfolio_return, 4),
        volatility=round(portfolio_volatility, 4),
        sharpe_ratio=sharpe_ratio,
        risk_level=risk_level
    )