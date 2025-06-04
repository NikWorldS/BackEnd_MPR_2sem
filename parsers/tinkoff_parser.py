import datetime as dt

import pandas as pd
import requests

from .data_parser import DataParser


class TinkoffParser(DataParser):
    def __init__(
        self,
        ticker: str,
        resolution: str,
        start: dt.datetime = None,
        end: dt.datetime = None,
    ) -> None:
        super().__init__(ticker, start, end)
        self.resolution = resolution

    def fetch_data(self):

        response = requests.get(
            "https://www.tbank.ru/api/trading/symbols/candles",
            {
                "from": self.start.isoformat(),
                "to": self.end.isoformat(),
                "ticker": self.ticker,
                "resolution": self.resolution,
            },
        )
        data = response.json()["payload"]["candles"]
        procesed_data = self._normalize_data(data)

        self._data = procesed_data
        return self.get_data()

    def get_data(self):
        return self._data.copy()

    def _normalize_data(self, data):
        df = pd.DataFrame(data)

        processed_data = df[["c", "date"]].copy()
        processed_data.columns = ["close", "date"]

        processed_data["date"] = pd.to_datetime(processed_data["date"], unit="s")
        processed_data.set_index("date", inplace=True)

        return processed_data
