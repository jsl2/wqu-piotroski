"""CLI interface for wqu_piotroski project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import click
import wqu_piotroski.adapter.za.share_data as za_share_data
import wqu_piotroski.adapter.za.piotroski as za_piotroski
import wqu_piotroski.adapter.ind.share_data as ind_share_data
import wqu_piotroski.adapter.ind.piotroski as ind_piotroski


@click.group()
@click.pass_context
def main(ctx):  # pragma: no cover
    """
    The main function executes on commands:
    `python -m wqu_piotroski` and `$ wqu_piotroski `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
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
