## Usage
To install the package CLI and all requirements:
```bash
cd wqu-piotroski
pip install -e .
```

The package SciencePlots requires an active LateX installation.

```bash
$ python -m wqu_piotroski
#or
$ wqu_piotroski
```

The CLI has the following commands:
- `wqu_piotroski get-data` fetches data from all sources and saves to pickle files in `wqu-piotroski/data`. This command does not work without adjustment to piotroski.py with headers/cookies for an active Finbox subscription, however all required data is commited to the repository, so running this command is not necessary, it is included just for reference.
- `wqu_piotroski fscore-stats` generates F-score statistics and plots: `IND-mean.png`, `IND-range.png`, `ZA-mean.png` and `ZA-range.png`
- `wqu_piotroski backtest` runs the backtest of the trading strategy and plots performance compared to benchmark in `IND-funds.png` and `ZA-funds.png`
