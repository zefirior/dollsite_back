"""Модуль содержит функционал соединения с базой данных."""

from app import app
from flask import g
import psycopg2 as pg


def get_db():
    """
    Open a new database connection.

    If there is none yet for the current application context.
    """
    if not hasattr(g, "site_db"):
        connection = pg.connect(
            dbname="dollsite",
            user="dollsite",
            password=app.config["DS_DB_PASSW"]
        )
        g.site_db = connection
    return g.site_db


@app.teardown_appcontext
def close_db(error):
    """Триггер закрывающий подключение к базе."""
    if hasattr(g, "site_db"):
        g.site_db.close()
