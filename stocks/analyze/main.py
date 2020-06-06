# Author David Li
# Description analyzes stocks based on current prices

from stocks.util import get_prices

import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
from mlfinlab.online_portfolio_selection.benchmarks import BAH, BestStock, BCRP, CRP
def generate_performance(
        stocks, 
        start_date="2020-03-01", 
        end_date="2020-05-30",
        title="Canadian Stocks",
        file_name="images/portfolio/cad_stocks.png"
    ):
    """
        Description: Generates performance charts for a given set of stocks
    """
    cad_df = get_prices(stocks, start_date, end_date)
    cad_df.columns = stocks
    cad_bah = BAH()
    cad_bah.allocate(cad_df)
    cad_beststock = BestStock()
    cad_beststock.allocate(cad_df)
    cad_crp = CRP()
    cad_crp.allocate(cad_df)
    cad_bcrp = BCRP()
    cad_bcrp.allocate(cad_df)
    fig = go.Figure()
    idx = cad_bah.portfolio_return.index
    fig.add_trace(go.Scatter(x=idx, y=cad_beststock.portfolio_return['Returns'], name="Best Stock"))
    fig.add_trace(go.Scatter(x=idx, y=cad_bah.portfolio_return['Returns'], name="Buy and Hold"))
    fig.add_trace(go.Scatter(x=idx, y=cad_crp.portfolio_return['Returns'], name="CRP"))
    fig.add_trace(go.Scatter(x=idx, y=cad_bcrp.portfolio_return['Returns'], name="BCRP"))
    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Relative Returns')
    pio.write_image(fig, file_name, scale=3)
    return file_name

from mlfinlab.portfolio_optimization import RiskMetrics
def generate_risk_stats(
        stocks,
        weights,
        alpha=0.05,
        start_date="2020-03-01", 
        end_date="2020-05-30",
    ):
    assets_returns = get_prices(stocks, start_date, end_date)
    # Calculate empirical covariance of assets
    assets_cov = assets_returns.cov()

    # Class that contains needed functions
    risk_met = RiskMetrics()

    # Calculate Variance
    Var = risk_met.calculate_variance(assets_cov, weights)

    # Calculate Value at Risk of the first asset
    VaR = risk_met.calculate_value_at_risk(assets_returns.iloc[:,0], alpha)

    # Calculate Expected Shortfall
    CVaR = risk_met.calculate_expected_shortfall(assets_returns.iloc[:,0], alpha)

    # Calculate Conditional Drawdown at Risk
    CDaR = risk_met.calculate_conditional_drawdown_risk(assets_returns.iloc[:,0], alpha)
    print(Var)
    print(VaR)
    print(CVaR)
    print(CDaR)
    return Var, VaR, CVaR, CDaR
