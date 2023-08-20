# constituents of BSE Sensex as of 17 Feb 2012 from wayback machine https://web.archive.org/web/20130509033530/https://en.wikipedia.org/wiki/BSE_SENSEX
import json
import requests
import pandas as pd
import pickle

constituents = [
    "500010",
    "500087",
    "500103",
    "500112",
    "500180",
    "500182",
    "500209",
    "500312",
    "500325",
    "500400",
    "500440",
    "500470",
    "500510",
    "500520",
    "500570",
    "500696",
    "500875",
    # "500900", 2013 merger
    "507685",
    "524715",
    "532155",
    "532174",
    "532286",
    "532454",
    "532500",
    "532540",
    "532555",
    "532868",
    "532977",
    "533278",
]


def get_share_data(scripcode):
    params = {
        "scripcode": scripcode,
        "flag": "1",
        "fromdate": "20130101",
        "todate": "20230801",
        "seriesid": "",
    }

    response = requests.get(
        "https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w",
        params=params,
    )
    data = response.json()
    data = json.loads(data["Data"])
    df = pd.DataFrame(data)
    df["dttm"] = pd.to_datetime(df["dttm"])
    df.set_index("dttm", inplace=True)
    return df


def get_all_share_data():
    share_data = {}
    for code in constituents:
        share_data[code] = get_share_data(code)
        print(f"Got data for {code}...")
    with open("wqu_piotroski/data/ind_share_data.pickle", "wb") as f:
        pickle.dump(share_data, f)
    return share_data
