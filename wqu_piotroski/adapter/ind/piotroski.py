import requests
from .share_data import constituents
import pickle


def get_all_piotroski():
    piotroski_data = {}
    for index in constituents:
        piotroski_data[index] = get_piotroski(index)
        print(f"Got data for {index}...")
    with open("wqu_piotroski/data/ind_piotroski_data.pickle", "wb") as f:
        pickle.dump(piotroski_data, f)
    return piotroski_data


def get_piotroski(ticker):
    cookies = {
        # login to finbox.com and paste cookies from request here
    }

    headers = {
        # login to finbox.com and paste headers from request here
    }

    assert (
        len(cookies) > 0
    ), "You must enter headers and cookies from a finbox.com sesion!"

    params = {
        "raw": "true",
    }

    json_data = {
        "query": "\nquery glossaryChart ($ticker: String!, $currency: String, $metric: String!, $period: String!) {\n  company (ticker: $ticker) {\n    glossary (currency: $currency, metric: $metric) {\n      chart(period: $period) {\n        subtype\n        type\n        metrics\n        full_tickers\n        data {\n          metric\n          metric_name\n          asset_name\n          values\n          period_dates\n          currency\n          ticker\n          full_ticker\n        }\n      }\n    }\n  }\n}\n",
        "variables": {
            "ticker": f"BSE:{ticker}",
            "metric": "piotroski_score",
            "currency": "presentment",
            "period": "FY",
        },
    }

    response = requests.post(
        "https://finbox.com/_/api/v5/query",
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response.json()["data"]["company"]["glossary"]["chart"]["data"]
