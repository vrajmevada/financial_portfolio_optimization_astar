import numpy as np
import pandas as pd

def portfolio_returns(weights,returns_df):
    weights=np.array(weights)
    return returns_df.values @ weights

def cumulative_pnl(portfolio_returns):
    return np.cumprod(1+portfolio_returns)-1

def annualized_return(portfolio_returns,periods_per_year=252):
    total_return=np.prod(1+portfolio_returns)
    years=len(portfolio_returns)/periods_per_year
    return total_return ** (1/years)-1

def annualized_volatility(portfolio_returns,periods_per_year=252):
    return np.std(portfolio_returns)**(1/periods_per_year)*np.sqrt(periods_per_year)

def sharpe_ratio(portfolio_returns , risk_free_rate=0.0,periods_per_year=252):
    excess_returns=portfolio_returns-risk_free_rate/periods_per_year
    return np.mean(excess_returns)/np.std(excess_returns)*np.sqrt(periods_per_year)

def max_drawdown(cumulative_pnl):
    running_max=np.maximum.accumulate(cumulative_pnl)
    drawdowns=(cumulative_pnl-running_max)
    return np.min(drawdowns)

