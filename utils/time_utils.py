from datetime import timedelta

RESOLUTION_TO_TIMEDELTA = {
    '1': timedelta(minutes=1),
    '5': timedelta(minutes=5),
    '10': timedelta(minutes=10),
    '15': timedelta(minutes=15),
    '30': timedelta(minutes=30),
    '60': timedelta(hours=1),
    '240': timedelta(hours=4),
    'D': timedelta(days=1),
    'W': timedelta(weeks=1),
    'M': timedelta(days=30),

}

def get_resolution(resolution: str) -> timedelta:
    return RESOLUTION_TO_TIMEDELTA.get(resolution)