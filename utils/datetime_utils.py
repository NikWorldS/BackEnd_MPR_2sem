from datetime import timedelta
from dateutil.relativedelta  import relativedelta
import numpy as np


RESOLUTION_TO_TIMEDELTA = {
    '1m': timedelta(minutes=1),
    '5m': timedelta(minutes=5),
    '10m': timedelta(minutes=10),
    '15m': timedelta(minutes=15),
    '30m': timedelta(minutes=30),
    '1h': timedelta(hours=1),
    '4h': timedelta(hours=4),
    '1D': timedelta(days=1),
    '1W': timedelta(weeks=1),
    '1M': relativedelta(months=1),
    '1Q': relativedelta(months=3)

}

def get_resolution(resolution: str) -> timedelta:
    return RESOLUTION_TO_TIMEDELTA.get(resolution)

def calculate_delta_time(dates: np.ndarray) -> np.ndarray:
    timesteps = dates.astype(np.int64)
    return np.diff(timesteps, prepend=timesteps[0]) // 10**9
