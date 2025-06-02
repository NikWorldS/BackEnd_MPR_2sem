import sys
import os

import redis
from flask import Flask
import psycopg2
from dotenv import load_dotenv

import routes
from services.news_analyzer import start_scheduler


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

        redis_cache = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
        )

    except Exception as ex:
        print("Ошибка базы данных:", repr(ex))
        sys.exit()

    app = Flask(__name__)

    routes.init(app, db_conn, redis_cache)

    return app


app = create_app()

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()
    app.run(debug=True)
