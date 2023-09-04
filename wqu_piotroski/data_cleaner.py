import logging
from datetime import datetime
import pickle

import pandas as pd
from wqu_piotroski.adapter.ind.share_data import IND_PICKLE_PATH
from wqu_piotroski.adapter.ind.piotroski import IND_PIOTROSKI_PATH
from wqu_piotroski.adapter.za.share_data import ZA_PICKLE_PATH
from wqu_piotroski.adapter.za.piotroski import ZA_PIOTROSKI_PATH


def load_pickle_data(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)


def finbox_piotroski_to_df(finbox_list):
    assert len(finbox_list) == 1, finbox_list
    df_dict = {
        "score": finbox_list[0]["values"],
        "date": finbox_list[0]["period_dates"],
    }
    df = pd.DataFrame(df_dict)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df


def load_data() -> dict:
    # clean share data
    # - make all share data have same start/end date
    # clean piotroski data
    # - make all piotroski score data have same start/end date
    all_data = {}
    starts = []
    ends = []
    for share_path, name in zip(
        [IND_PICKLE_PATH, ZA_PICKLE_PATH], ["ind_share", "za_share"]
    ):
        all_data[name] = load_pickle_data(share_path)
        start, end = get_start_end(all_data[name])
        starts.append(start)
        ends.append(end)

    start = max(starts)
    end = min(ends)
    for share_path, name in zip(
        [IND_PICKLE_PATH, ZA_PICKLE_PATH], ["ind_share", "za_share"]
    ):
        logging.info(f"Cropping date range for {name} to {start}:{end}")
        for ticker in all_data[name]:
            df = all_data[name][ticker]
            df.rename(columns={"vale1": "close", "vole": "volume"}, inplace=True)
            df = df.astype(float)
            all_data[name][ticker] = df[start:end]

    for piotroski_path, share_name, name in zip(
        [IND_PIOTROSKI_PATH, ZA_PIOTROSKI_PATH],
        ["ind_share", "za_share"],
        ["ind_piotroski", "za_piotroski"],
    ):
        logging.info(f"Loading piotroski date range for {name}")
        piotroski_data = load_pickle_data(piotroski_path)
        for ticker in piotroski_data:
            finbox_list = piotroski_data[ticker]
            piotroski_data[ticker] = finbox_piotroski_to_df(finbox_list)
        all_data[name] = piotroski_data
        start, end = get_start_end(all_data[name])
        logging.info(f"Cropping date range for {name} to {start}:{end}")
        for ticker in all_data[name]:
            df = all_data[name][ticker]
            all_data[name][ticker] = df[start:end]
        check_data_dicts(all_data[name], all_data[share_name])
    return all_data


def check_data_dicts(piotroski_dict, share_dict):
    # - ensure same number of elements in each stock
    # - ensure all stock symbols shared across piotroski and share data
    start_dates = set([df.index[0] for df in piotroski_dict.values()])
    end_dates = set([df.index[-1] for df in piotroski_dict.values()])
    lengths = set([len(df) for df in piotroski_dict.values()])
    assert len(start_dates) == 1, start_dates
    assert len(end_dates) == 1, end_dates
    assert len(lengths) == 1, lengths
    assert sorted(list(piotroski_dict.keys())) == sorted(
        list(share_dict.keys())
    ), "Keys between piotroski and share dict do not match!"


def get_start_end(data_dict):
    start_date = get_max_start_date(data_dict)
    end_date = get_min_end_date(data_dict)
    return start_date, end_date


def get_min_end_date(dict_df):
    min_date = datetime.today()
    for ticker in dict_df:
        if dict_df[ticker].index[-1] < min_date:
            min_date = dict_df[ticker].index[-1]
    return min_date


def get_max_start_date(dict_df):
    max_date = datetime.fromtimestamp(0)
    for ticker in dict_df:
        if dict_df[ticker].index[0] > max_date:
            if dict_df[ticker].index[0] > datetime(2015, 1, 1):
                print(ticker)
            max_date = dict_df[ticker].index[0]
    return max_date
