from dotenv import load_dotenv
from flask import Flask
import psycopg2
import redis
import sys
import os

import routes
from utils.redis_config import get_redis_url
from services.tasks import analyze_news_task

def create_app():
    load_dotenv()

    db_conn = None

    try:
        db_conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )

        redis_cache = redis.Redis.from_url(get_redis_url())

    except Exception as ex:
        print("Ошибка базы данных:", repr(ex))
        sys.exit()

    app = Flask(__name__)

    routes.init(app, db_conn, redis_cache)

    return app


app = create_app()

if __name__ == "__main__":
    if not os.path.exists("metals_news.json"):
        analyze_news_task.delay()
    app.run(debug=True)
