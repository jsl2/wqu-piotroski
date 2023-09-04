"""
Data structure:
{
    "ind_share": {
        "ticker1": pd.DataFrame(columns=['vale1','vole']) # close price, volume
        ...
    },
    "ind_piotroski": {
        "ticker1": pdDataFrame(columns=['score']) # quarterly piotroski scores
        ...
    }
}
"""
from datetime import datetime
import logging
from matplotlib import pyplot as plt
import pandas as pd
import scienceplots

plt.style.use(["science", "ieee"])
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times"]})


def get_closest_date_after(target_date, dates):
    for date in sorted(dates):
        if date < target_date:
            continue
        return date
    raise ValueError("No date after target date available")


def get_stocks_scores(piotroski_data):
    """Go through all quarterly piotroski data to select stocks
    to long and short at each quarter start.
    """
    stocks = {}
    for ticker in piotroski_data:
        for i in range(len(piotroski_data[ticker])):
            date = piotroski_data[ticker].index[i]
            score = piotroski_data[ticker].iloc[i]["score"]
            if date not in stocks:
                stocks[date] = {}
            if score not in stocks[date]:
                stocks[date][score] = []
            stocks[date][score].append(ticker)
    return stocks


def get_short_long(scores):
    # given dict of scores->list of tickers, select
    # first at x least 3 'worst score' stocks to short
    # then select at least 5 'best score' stocks to long
    short_stocks = []
    long_stocks = []

    for i in range(1, 10):
        if i not in scores:
            continue
        short_stocks.extend(scores[i])
        if len(short_stocks) > 2:
            break
    for i in range(9, 0, -1):
        if i not in scores:
            continue
        long_stocks.extend(scores[i])
        if len(long_stocks) > 4:
            break
    return short_stocks, long_stocks


def perform_portfolio_actions(
    portfolio, start_date, funds, quarter_date, stocks_scores, share_data
):
    new_portfolio = {}
    if len(portfolio) > 0:
        funds *= close_portfolio(portfolio, start_date, quarter_date, share_data)
    shorts, longs = get_short_long(stocks_scores[quarter_date])
    logging.debug(
        f"Quarter {datetime.strftime(quarter_date, '%Y-%m-%d')}: short: {len(shorts)} long: {len(longs)}"
    )
    short_weight = -1 / len(shorts)
    long_weight = 2 / len(longs)
    new_portfolio = {short_stock: short_weight for short_stock in shorts}
    new_portfolio.update({long_stock: long_weight for long_stock in longs})
    return new_portfolio, funds


def close_portfolio(portfolio, start_date, end_date, share_data):
    """Returns relative change i.e. 1.1 for 10% growth"""
    net = 0.0
    net_weight = 0.0
    for ticker in portfolio:
        trading_day_start_date = get_closest_date_after(
            start_date, share_data[ticker].index
        )
        trading_day_end_date = get_closest_date_after(
            end_date, share_data[ticker].index
        )

        pct_change = (
            float(share_data[ticker]["close"][trading_day_end_date])
            - float(share_data[ticker]["close"][trading_day_start_date])
        ) / float(share_data[ticker]["close"][trading_day_start_date])
        net += portfolio[ticker] * (1 + pct_change)
        net_weight += portfolio[ticker]
    return net


def get_strategy_profits(stocks_scores, share_data, country):
    portfolio1 = {}
    portfolio1_start = None
    portfolio1_funds = 0.5
    portfolio2 = {}
    portfolio2_start = None
    portfolio2_funds = 0.5
    benchmark_funds = 1.0
    funds = {}
    quarters = list(sorted(stocks_scores.keys()))
    for quarter1, quarter2 in zip(quarters[::2], quarters[1::2]):
        portfolio1, portfolio1_funds = perform_portfolio_actions(
            portfolio1,
            portfolio1_start,
            portfolio1_funds,
            quarter1,
            stocks_scores,
            share_data,
        )
        benchmark_funds *= get_avg_return(portfolio2_start, quarter1, share_data)
        funds[quarter1] = {
            "Benchmark": benchmark_funds,
            "Long-short strategy": portfolio1_funds + portfolio2_funds,
        }
        portfolio1_start = quarter1
        # portfolio 2 buy/sell on odd index quarters
        portfolio2, portfolio2_funds = perform_portfolio_actions(
            portfolio2,
            portfolio2_start,
            portfolio2_funds,
            quarter2,
            stocks_scores,
            share_data,
        )
        benchmark_funds *= get_avg_return(quarter1, quarter2, share_data)
        funds[quarter2] = {
            "Benchmark": benchmark_funds,
            "Long-short strategy": portfolio1_funds + portfolio2_funds,
        }
        portfolio2_start = quarter2

    logging.info(
        f"Overall {country} portfolio growth: {portfolio1_funds + portfolio2_funds:.2f}"
    )
    logging.info(f"Overall {country} benchmark growth: {benchmark_funds:.2f}")
    df = pd.DataFrame(funds).transpose()
    ax = df.plot(title=f"{country} stocks")
    fig = ax.get_figure()
    fig.savefig(f"{country}-funds.png")
    fig.clear()
    return portfolio1_funds + portfolio2_funds


def get_avg_return(start, end, share_data):
    weight = 1 / len(share_data)
    ret = 0.0
    if start is None:
        return 1
    for ticker in share_data:
        start_date = get_closest_date_after(start, share_data[ticker].index)
        end_date = get_closest_date_after(end, share_data[ticker].index)
        start_price = share_data[ticker]["close"][start_date]
        end_price = share_data[ticker]["close"][end_date]
        ret += weight * (end_price / start_price)
    return ret
