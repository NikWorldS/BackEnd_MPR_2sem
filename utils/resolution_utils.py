INTERNAL_RESOLUTION = ["1m", "5m", "10m", "15m", "30m", "1h", "4h", "1D", "1W", "1M", "1Q"]

EXCHANGE_RESOLUTION_MAP = {
    "TINKOFF": {
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1D": "D",
        "1W": "W",
        "1M": "M"

    },
    "MOEX": {
        "1m": "1",
        "10m": "10",
        "1h": "60",
        "1D": "24",
        "1W": "7",
        "1M": "31",
        "1Q": "4"
    },
    "SBER":{
        "1D": "D",
        "1W": "W",
        "1M": "M",
    },
}

def get_exchange_resolution(sec_id: str, internal_res: str) -> str:
    return EXCHANGE_RESOLUTION_MAP[sec_id].get(internal_res)
