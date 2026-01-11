import seaborn as sns
import matplotlib.pyplot as plt

from src.data_loader import load_price_data, compute_log_returns

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
start = "2021-01-01"
end = "2025-01-01"

prices = load_price_data(tickers, start, end)
returns = compute_log_returns(prices)

corr = returns.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Asset Correlation Heatmap")
plt.tight_layout()
plt.savefig("results/correlation_heatmap.png")
plt.show()
