import numpy as np
import pandas as pd
import yfinance as yf

def load_price_data(tickers,start_data,end_data):
    data=yf.download(
        tickers,
        start=start_data,
        end=end_data,
        progress=False,
        auto_adjust=True
    )
    if isinstance(data.columns,pd.MultiIndex):
        prices=data['Close']
    else:
        prices=data['Close']

    prices=prices.dropna()
    return prices

def compute_log_returns(price_data):
    log_returns = np.log(price_data/price_data.shift(1))
    log_returns = log_returns.dropna()
    return log_returns

def compute_mean_returns(log_returns):
    return log_returns.mean()

def compute_covariance_matrix(log_returns):
    return log_returns.cov()

def compute_correlation_matrix(log_returns):
    return log_returns.corr()

def save_processed_data(price_data,log_returns,output_dir="data"):
    price_data.to_csv(f"{output_dir}/prices.csv")
    log_returns.to_csv(f"{output_dir}/returns.csv")

if __name__ == "__main__":
    ticker = ["AAPL","MSFT","GOOGL","AMZN","META"]
    start="2021-01-01"
    end="2025-01-01"

    prices = load_price_data(ticker,start,end)
    returns = compute_log_returns(prices)

    mu = compute_mean_returns(returns)
    cov=compute_covariance_matrix(returns)
    corr = compute_correlation_matrix(returns)

    save_processed_data(prices,returns)

    print("Mean Returns:")
    print(mu)
    print("\nCovariance Matrix:")
    print(cov)