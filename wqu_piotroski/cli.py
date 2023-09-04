"""CLI interface for wqu_piotroski project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import logging
import click
import wqu_piotroski.adapter.za.share_data as za_share_data
import wqu_piotroski.adapter.za.piotroski as za_piotroski
import wqu_piotroski.adapter.ind.share_data as ind_share_data
import wqu_piotroski.adapter.ind.piotroski as ind_piotroski
from .base import load_data
from .back_tester import get_stocks_scores, get_strategy_profits
from .stats import plot_scores, get_scores_returns


@click.group()
@click.pass_context
def main(ctx):  # pragma: no cover
    """
    The main function executes on commands:
    `python -m wqu_piotroski` and `$ wqu_piotroski `.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s")
    ctx.ensure_object(dict)


@main.command()
@click.pass_context
def get_data(ctx):
    print("Getting BSE Sensex historical price data for IND from BSE")
    print(ind_share_data.get_all_share_data())
    print("Getting BSE Sensex historical piotroski scores for IND from BSE")
    ind_piotroski.get_all_piotroski()
    print("Getting top 40 historical price data for ZA from JSE")
    za_share_data.get_all_share_data()
    print("Getting top 40 historical piotroski scores for ZA from JSE")
    za_piotroski.get_all_piotroski()


@main.command()
@click.pass_context
def backtest(ctx):
    all_data = load_data()

    ind_stocks_scores = get_stocks_scores(all_data["ind_piotroski"])
    growth = get_strategy_profits(ind_stocks_scores, all_data["ind_share"], "IND")
    za_stocks_scores = get_stocks_scores(all_data["za_piotroski"])
    growth = get_strategy_profits(za_stocks_scores, all_data["za_share"], "ZA")


@main.command()
@click.pass_context
def fscore_stats(ctx):
    all_data = load_data()
    plot_scores(all_data["za_piotroski"], "ZA")
    plot_scores(all_data["ind_piotroski"], "IND")
    ind_stocks_scores = get_stocks_scores(all_data["ind_piotroski"])
    za_stocks_scores = get_stocks_scores(all_data["za_piotroski"])
    get_scores_returns(all_data["za_share"], za_stocks_scores, "ZA")
    get_scores_returns(all_data["ind_share"], ind_stocks_scores, "IND")
