import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_price_data, compute_log_returns
from src.optimizer import optimize_portfolio
from src.metrics import (
    portfolio_returns,
    cumulative_pnl,
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown
)

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
start = "2021-01-01"
end = "2025-01-01"

prices = load_price_data(tickers, start, end)
returns = compute_log_returns(prices)

split = int(0.7 * len(returns))
train_returns = returns.iloc[:split]
test_returns = returns.iloc[split:]

mu = train_returns.mean().values
cov = train_returns.cov().values

result = optimize_portfolio(mu, cov, risk_aversion=0.3)
weights = result["optimal_weights"]

test_portfolio_returns = portfolio_returns(weights, test_returns)
pnl = cumulative_pnl(test_portfolio_returns)

print("Optimized Portfolio Metrics")
print("----------------------------")
print("Weights:", weights)
print("Annualized Return:", annualized_return(test_portfolio_returns))
print("Annualized Volatility:", annualized_volatility(test_portfolio_returns))
print("Sharpe Ratio:", sharpe_ratio(test_portfolio_returns))
print("Max Drawdown:", max_drawdown(pnl))

equal_weights = np.array([1 / len(weights)] * len(weights))
baseline_returns = portfolio_returns(equal_weights, test_returns)
baseline_pnl = cumulative_pnl(baseline_returns)

print("\nEqual Weight Portfolio")
print("----------------------")
print("Sharpe Ratio:", sharpe_ratio(baseline_returns))
print("Max Drawdown:", max_drawdown(baseline_pnl))

plt.figure(figsize=(10, 6))
plt.plot(pnl, label="A* Optimized Portfolio")
plt.plot(baseline_pnl, label="Equal Weight Portfolio", linestyle="--")
plt.title("Cumulative PnL Comparison")
plt.xlabel("Time")
plt.ylabel("PnL")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/pnl_curve.png")
plt.show()
import json

summary = {
    "optimized": {
        "weights": list(weights),
        "annualized_return": annualized_return(test_portfolio_returns),
        "annualized_volatility": annualized_volatility(test_portfolio_returns),
        "sharpe_ratio": sharpe_ratio(test_portfolio_returns),
        "max_drawdown": max_drawdown(pnl),
    },
    "equal_weight": {
        "sharpe_ratio": sharpe_ratio(baseline_returns),
        "max_drawdown": max_drawdown(baseline_pnl),
    }
}

with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=4)


