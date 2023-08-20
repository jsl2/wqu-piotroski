"""Helpers for scraping share data for JSE stocks from sharedata.co.za"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle


def get_stock_indices():
    response = requests.get(
        "https://www.sharedata.co.za/V2/Controls/Shares/ShareIndex/SIJSONData.aspx",
        params={"indextype": "TOP40", "sortfield": "FULLNAME"},
    )
    soup = BeautifulSoup(response.content, "html.parser")
    trs = soup.find_all("tr", class_="TableRowHighLight_OnHover")
    indices = [tr.td.text for tr in trs]
    return indices


def get_share_data(ticker):
    json_data_url = (
        "https://www.sharedata.co.za/V2/Controls/Chart/InteractiveChart/JSONdata.aspx"
    )
    columns = ["date", "open", "close", "volume"]
    share_data = {}
    for column in columns:
        response = requests.get(
            json_data_url, params={"c": ticker, "All": "ALL", "p": column}
        )
        share_data[column] = response.json()

    df = pd.DataFrame(share_data)
    df["date"] = pd.to_datetime(df["date"], unit="ms")
    df.set_index("date", inplace=True)
    return df


def get_all_share_data():
    share_data = {}
    for index in get_stock_indices():
        share_data[index] = get_share_data(index)
        print(f"Got data for {index}...")
    with open("wqu_piotroski/data/za_share_data.pickle", "wb") as f:
        pickle.dump(share_data, f)
    return share_data
