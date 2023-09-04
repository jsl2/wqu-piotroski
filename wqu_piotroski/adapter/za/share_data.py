"""Helpers for scraping share data for JSE stocks from sharedata.co.za"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

ZA_PICKLE_PATH = "wqu_piotroski/data/za_share_data.pickle"

constituents = [
    "JSE:BTI",
    # "JSE:SAB",
    "JSE:BHG",
    "JSE:CFR",
    "JSE:AGL",
    "JSE:MTN",
    "JSE:NPN",
    "JSE:SOL",
    "JSE:SBK",
    "JSE:VOD",
    "JSE:KIO",
    "JSE:FSR",
    # "JSE:OMU",
    "JSE:ABG",
    "JSE:SLM",
    "JSE:SHP",
    "JSE:REM",
    "JSE:NED",
    "JSE:APN",
    "JSE:AMS",
    "JSE:BVT",
    "JSE:ANG",
    "JSE:IMP",
    "JSE:WHL",
    "JSE:TBS",
    # "JSE:MDC",
    "JSE:EXX",
    "JSE:RMH",
    # "JSE:ITU",
    "JSE:GRT",
    "JSE:DSY",
    "JSE:GFI",
    "JSE:MNP",
    "JSE:SNH",
    # "JSE:ASR",
    "JSE:INP",
    # "JSE:MSM"
    # "JSE:IPL",
    "JSE:TRU",
    "JSE:ARI",
    "JSE:INL",
    # "JSE:MND"
]


def get_share_data(ticker):
    json_data_url = (
        "https://www.sharedata.co.za/V2/Controls/Chart/InteractiveChart/JSONdata.aspx"
    )
    columns = ["date", "open", "close", "volume"]
    share_data = {}
    for column in columns:
        response = requests.get(
            json_data_url, params={"c": ticker[4:], "All": "ALL", "p": column}
        )
        share_data[column] = response.json()

    df = pd.DataFrame(share_data)
    df["date"] = pd.to_datetime(df["date"], unit="ms")
    df.set_index("date", inplace=True)
    return df


def get_all_share_data():
    share_data = {}
    for index in constituents:
        share_data[index] = get_share_data(index)
        print(f"Got data for {index}...")
    with open(ZA_PICKLE_PATH, "wb") as f:
        pickle.dump(share_data, f)
    return share_data
