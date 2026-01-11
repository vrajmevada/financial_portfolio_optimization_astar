# Financial Portfolio Optimization using A* Search

## Overview
This project implements an **portfolio optimization system** using **A\* search** to construct optimal asset allocations under risk–return constraints.  
The system formulates portfolio selection as a **state-space search problem**, where candidate portfolios are explored using an informed heuristic to efficiently identify allocations that improve profitability while controlling risk.

The optimization engine is exposed through a **Django REST API**, and results are analyzed using an **interactive analytics dashboard**.  
Performance is evaluated quantitatively using **cumulative PnL, Sharpe ratio, drawdown**, and **baseline comparison**.

### State Representation

Each state represents a candidate portfolio allocation:

w = [w₁, w₂, …, wₙ],   where Σ wᵢ = 1


Each state corresponds to a feasible allocation across assets.

### Actions
An action transitions between state by:
1) Incrementally adjusting asset weight
2) Re-normalizing allocations to maintain constraints
This allows systematic exploration of the portfolio space.

### Cost Function
The A* cost function balances risk and return 
Cost = Portfolio Variance - λ × Expected Return 
Where:
1) Portfolio variance incorporates asset correlations
2) Expected return is derived from historical returns
3) λ(risk aversion) controls the risk-return tradeoff
Lower cost corresponds to better risk-adjusted portfolios.

### Heuristic Function
The heuristic estimates remaining improvement potential by:
1) Penalizing high volatility
2) Rewarding higher expected return
This heuristic guides the search toward promising allocations, significantly reducing the search space while maintaining solution quality.

### Why A* Works well for Portfolio Optimization
1) Explicit control over constraints
2) Efficient exploration of large allocation spaces
3) Deterministic and explainable decision process
4) Naturally integrates financial objectives into search cost 

## Performance Evaluation & PnL Impact
### Baseline Comparision
To validate effectiveness, the optimized portfolio is benchmarked against an equal-weight portfolio.
This ensures improvements are due to the optimization strategy rather than market movement alone.

### Metrics Used
1) Cumulative PnL – total profitability over time
2) Sharpe Ratio – risk-adjusted return
3) Maximum Drawdown – downside risk exposure
4) Correlation Matrix – diversification effectiveness

### Observed Impact on PnL
1) A* optimization improves risk-adjusted returns compared to baseline
2) Correlation-aware allocation reduces drawdowns
3) Portfolio weights adapt to balance diversification and return
4) Risk-aversion parameter directly influences PnL stability

### Dashboard & Visualization
An interactive analytics dashboard provides:
1) Optimized vs baseline PnL comparison
2) Sharpe ratio and final PnL comparison
3) Correlation heatmap across assets
4) Real-time re-evaluation with different parameters

### Tech Stack
1) Python
2) Django - backend API
3) NiceGUI - analytics dashboard
4) NumPy / Pandas - numerical computation
5) Echarts- interactive visualization
6) yFinance - market data

## Conclusion 
This project demonstrates how A* search can be effectively applied to financial portfolio optimization, producing measurable improvements in PnL and risk-adjusted performance while maintaining a clean, modular backend architecture.

---


