import os
from dotenv import load_dotenv

load_dotenv()

def get_redis_url():
    """returns redis url for connecting"""
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")
    db = os.getenv("REDIS_DB")

    return f"redis://{host}:{port}/{db}"