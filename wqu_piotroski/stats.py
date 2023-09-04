import logging
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import scienceplots
from .back_tester import get_closest_date_after
from dateutil.relativedelta import relativedelta
from scipy import stats

plt.style.use(["science", "ieee"])
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times"]})


def plot_scores(fscores, country):
    n_stocks = len(fscores)
    key0 = list(fscores.keys())[0]
    all_stats = {}
    for date in fscores[key0].index:
        stats = {"mean": 0.0, "F-score $\leqslant$ 2": 0, "F-score $\geqslant$ 8": 0}
        for stock in fscores:
            stats["mean"] += fscores[stock]["score"][date] / n_stocks
            stats["F-score $\leqslant$ 2"] = (
                stats["F-score $\leqslant$ 2"] + 1.0 / n_stocks
                if fscores[stock]["score"][date] < 3
                else stats["F-score $\leqslant$ 2"]
            )
            stats["F-score $\geqslant$ 8"] = (
                stats["F-score $\geqslant$ 8"] + 1.0 / n_stocks
                if fscores[stock]["score"][date] > 7
                else stats["F-score $\geqslant$ 8"]
            )
        all_stats[date] = stats
    df = pd.DataFrame(all_stats).transpose()
    ax = df["mean"].plot(title=f"Mean F-Score for {country} stocks")
    fig = ax.get_figure()
    fig.savefig(f"{country}-mean.png")
    fig.clear()

    ax = df[["F-score $\leqslant$ 2", "F-score $\geqslant$ 8"]].plot(
        title=f"High and low bin F-Score for {country} stocks"
    )
    fig = ax.get_figure()
    fig.savefig(f"{country}-range.png")
    fig.clear()


def get_year_return(fiscal_quarter, stock_data):
    start_price = stock_data["close"][
        get_closest_date_after(fiscal_quarter, stock_data.index)
    ]
    end_price = stock_data["close"][
        get_closest_date_after(
            fiscal_quarter + relativedelta(years=1), stock_data.index
        )
    ]
    return 100 * ((end_price / start_price) - 1)


def get_scores_returns(share_data, stocks_scores, country):
    lt3_returns = []
    gt7_returns = []
    other_returns = []
    for fiscal_quarter in stocks_scores:
        try:
            for i in stocks_scores[fiscal_quarter]:
                if i < 4:
                    for ticker in stocks_scores[fiscal_quarter][i]:
                        lt3_returns.append(
                            get_year_return(fiscal_quarter, share_data[ticker])
                        )
                elif i > 6:
                    for ticker in stocks_scores[fiscal_quarter][i]:
                        gt7_returns.append(
                            get_year_return(fiscal_quarter, share_data[ticker])
                        )
                else:
                    for ticker in stocks_scores[fiscal_quarter][i]:
                        other_returns.append(
                            get_year_return(fiscal_quarter, share_data[ticker])
                        )
        except ValueError:
            logging.warning(f"{fiscal_quarter} too late (no stock date for close)")
            break

    print(country)
    print(f"<=3 {np.mean(lt3_returns):.2f} ({np.std(lt3_returns):.2f})")
    print(f">=7 {np.mean(gt7_returns):.2f} ({np.std(gt7_returns):.2f})")
    print(stats.ttest_ind(lt3_returns, gt7_returns, equal_var=False))
    all_returns = lt3_returns + gt7_returns + other_returns
    print(f"avg {np.mean(all_returns):.2f} ({np.std(all_returns):.2f})")
