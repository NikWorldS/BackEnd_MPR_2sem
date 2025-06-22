from typing import List, Any
import datetime as dt
import requests
import pandas as pd

from .data_parser import DataParser


class MoexParser(DataParser):
    def __init__(self, ticker: str, resolution: str, start: dt.datetime = None, end: dt.datetime = None) -> None:
        super().__init__(ticker, start, end)
        self.resolution = resolution
        self.url = f"https://iss.moex.com/iss/engines/currency/markets/selt/boardgroups/13/securities/{self.ticker}/candles.json"

    def _fetch_data(self, start) -> list:
        response = requests.get(self.url, params={
            "interval": self.resolution,
            "from": self.start.strftime('%Y-%m-%d'),
            "till": self.end.strftime('%Y-%m-%d'),
            "start": start
        })
        return response.json()["candles"]["data"]

    def fetch_data(self) -> pd.DataFrame:
        all_data = []
        start = 0
        while True:
            data = self._fetch_data(start)
            all_data.extend(data)
            start += len(data)
            if not data:
                break
        return self._normalize_data(all_data)

    def _normalize_data(self, data: List[List[Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)[[1, 7]]
        df.columns = ["close", "date"]
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        return df
