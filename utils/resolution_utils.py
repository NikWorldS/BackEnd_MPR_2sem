EXCHANGE_RESOLUTIONS = {
    "TINKOFF": ["5", "15", "30", "60", "240", "D", "W", "M"],
    "MOEX": ["1", "10", "60", "D", "W", "M"],
}

def is_valid_resolution(sec_id: str, resolution: str) -> bool:
    allowed = EXCHANGE_RESOLUTIONS.get(sec_id.upper())
    return allowed is not None and resolution in allowed