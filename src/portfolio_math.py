import numpy as np

def portfolio_return(weights,mean_returns):
    weights=np.array(weights)
    mean_returns=np.array(mean_returns)
    return np.dot(weights,mean_returns)

def portfolio_volatility(weights,covariance_matrix):
    weights=np.array(weights)
    covariance_matrix=np.array(covariance_matrix)
    variance=np.dot(weights.T,np.dot(covariance_matrix,weights))
    return np.sqrt(variance)

def portfolio_score(weights,mean_returns,covariance_matrix,risk_aversion=0.3):
    ret=portfolio_return(weights,mean_returns)
    vol=portfolio_volatility(weights,covariance_matrix)
    return ret-risk_aversion*vol

def validate_weights(weights,tol=1e-6):
    weights=np.array(weights)
    if np.any(weights<0):
        return False
    if abs(np.sum(weights)-1.0)>tol:
        return False
    return True

