import sys
import os

from flask import Flask
import psycopg2
from dotenv import load_dotenv

import routes


def main():
    load_dotenv()

    db_conn = None

    try:
        db_conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
    except Exception as ex:
        print("Ошибка базы данных:", repr(ex))
        sys.exit()

    app = Flask(__name__)

    routes.init(app, db_conn)

    app.run(debug=True)


if __name__ == "__main__":
    main()
