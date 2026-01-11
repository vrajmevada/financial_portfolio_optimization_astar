from django.shortcuts import render

# Create your views here.
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from src.data_loader import load_price_data,compute_log_returns
from src.optimizer import optimize_portfolio
from src.metrics import(
    portfolio_returns,
    cumulative_pnl,
    sharpe_ratio,
    max_drawdown
)
@csrf_exempt
def optimize_api(request):
    if request.method!="POST":
        return JsonResponse({"error":"POST request required"},status=400)
    data=json.loads(request.body)

    tickers=data.get("tickers",[])
    risk_aversion=float(data.get("risk_aversion",0.3))

    if len(tickers)<2:
        return JsonResponse({"error": "At leat 2 tickers required"},status=400)
    prices=load_price_data(tickers,"2021-01-01","2025-01-01")
    returns=compute_log_returns(prices)

    split=int(0.7*len(returns))
    returns=compute_log_returns(prices)

    split=int(0.7*len(returns))
    train=returns.iloc[:split]
    test=returns.iloc[split:]

    mu=train.mean().values
    cov=train.cov().values

    result=optimize_portfolio(mu,cov,risk_aversion)
    weights=result["optimal_weights"]

    port_returns=portfolio_returns(weights,test)
    pnl=cumulative_pnl(port_returns)
    import numpy as np
    n=len(weights)
    equal_weights=np.array([1.0/n]*n)
    baseline_returns=portfolio_returns(equal_weights,test)
    baseline_pnl=cumulative_pnl(baseline_returns)
    baseline_sharpe=sharpe_ratio(baseline_returns)

    response={
        "tickers":tickers,
        "weights":dict(zip(tickers,weights)),
        "sharpe":sharpe_ratio(port_returns),
        "max_drawdown":max_drawdown(pnl),
        "final_pnl":float(pnl[-1]),
        "pnl_series":pnl.tolist(),
        "baseline_sharpe":baseline_sharpe,
        "baseline_pnl_series":baseline_pnl.tolist(),
        "correlation":returns.corr().values.tolist()

    }
    return JsonResponse(response)