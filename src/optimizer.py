import itertools
import numpy as np
from src.astar import astar
from src.portfolio_math import (
    portfolio_score,
    validate_weights
)

def generate_neighbors(state,step=0.05):
    neighbors = []
    n=len(state)
    for i in range(n):
         for j in range(n):
             if i==j:
                 continue
             new_state=list(state)
             new_state[i]-=step
             new_state[j]+=step

             if validate_weights(new_state):
                 neighbors.append(tuple(new_state))

    return neighbors

def make_cost_fn(mean_returns,covariance_matrix,risk_aversion):
    def cost_fn(state):
        score=portfolio_score(
            state,
            mean_returns,
            covariance_matrix,
            risk_aversion
        )
        return -score
    return cost_fn

def make_heuristic_fn(mean_returns):
    best_return =np.max(mean_returns)
    def heuristic_fn(state):
        current_return =np.dot(state,mean_returns)
        return -(best_return - current_return)
    return heuristic_fn

def initial_state(num_assets):
    weight=1.0/num_assets
    return tuple([weight]*num_assets)

def optimize_portfolio(
        mean_returns,
        covariance_matrix,
        risk_aversion=0.3,
        step=0.05,
        max_iterations=5000
):
    num_assets=len(mean_returns)
    start_state=initial_state(num_assets)

    cost_fn=make_cost_fn(mean_returns,covariance_matrix,risk_aversion)
    heuristic_fn=make_heuristic_fn(mean_returns)

    def neighbor_fn(state):
        return generate_neighbors(state,step)

    path,final_node=astar(
        start_state=start_state,
        neighbor_fn=neighbor_fn,
        cost_fn=cost_fn,
        heuristic_fn=heuristic_fn,
        max_iterations=max_iterations
    )
    return{
        "optimal_weights":final_node.state,
        "score":-final_node.g,
        "path":path
    }


