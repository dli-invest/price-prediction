# Wrapper class so I can generate reports
# without having mlfinlab installed locally
import os
try:
    from stocks.analyze import generate_risk_stats,\
      generate_performance, generate_estimated_returns, \
      generate_portfolio_allocations
    mlfinlabExists = True
except ImportError as e:
    print(e)
    mlfinlabExists = False

def make_risk_metrics(
      stocks,
      weights,
      start_date,
      end_date
    ):
    """
      Parameters:
          stocks: List of tickers compatiable with the yfinance module
          weights: List of weights, probably going to be evenly distributed
    """
    if mlfinlabExists:
      Var, VaR, CVaR, CDaR = generate_risk_stats(
        stocks,
        weights,
        start_date=start_date,
        end_date=end_date
      )
    else:
      Var, VaR, CVaR, CDaR = 0,0,0,0
    return [
        {
          "value": Var,
          "name": "Variance",
          "description": "This measure can be used to compare portfolios" \
            " based on estimations of the volatility of returns."
        },
        {
          "value": VaR,
          "name": "Value at Risk",
          "description": "This measure can be used to compare portfolios" \
            " based on the amount of investments that can be lost in the next observation, assuming the returns for assets follow a multivariate normal distribution."
        },
        {
          "value": CVaR,
          "name": "Expected Shortfall",
          "description": "This measure can be used to compare portfolios" \
            " based on the average amount of investments that can be lost in a worst-case scenario, assuming the returns for assets follow a multivariate normal distribution."
        },
        {
          "value": CDaR,
          "name": "Conditional Drawdown at Risk",
          "description": "This measure can be used to compare portfolios"
            " based on the average amount of a portfolio drawdown in a worst-case scenario, assuming the drawdowns follow a normal distribution."
        }
    ]

def make_performance_plot(
        stocks, 
        start_date="2020-03-01", 
        end_date="2020-05-30",
        title="Canadian Stocks",
        file_name="images/portfolio/cad_stocks.png"
    ):
    """
      Description wrapper to tries to make an plot
    """
    if mlfinlabExists:
      return generate_performance(
        stocks, 
        start_date=start_date, 
        end_date=end_date,
        title=title,
        file_name=file_name
      )
    return None

def make_estimated_returns(
        stocks, 
        start_date="2020-03-01", 
        end_date="2020-05-30",
    ):
    if mlfinlabExists:
        return generate_estimated_returns(stocks, start_date, end_date)
    return [None, None]

def make_portfolio_allocations(
        stocks,
        portfolio_opt,
        start_date="2020-03-01", 
        end_date="2020-05-30",
        *other_settings
    ):
    if mlfinlabExists:
        return generate_portfolio_allocations(
          stocks, 
          portfolio_opt,
          start_date,
          end_date,
          *other_settings
        )
    return []
