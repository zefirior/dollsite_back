"""Модуль содержит правила роутинга приложения."""

import os

from app import app
from db import get_db
from flask import (
    abort,
    jsonify,
    request,
    send_file,
)
from json_methods import collections_bublics, get_lot


@app.route('/lot', methods=['GET'])
def lot():
    """Информация о лотах."""
    lot_id = request.args.get('lot_id', None)
    response = jsonify(get_lot(lot_id))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/collections/bublics', methods=['GET'])
def bublics():
    """Информация о бубликах."""
    page = request.args.get('page', None)
    response = jsonify(collections_bublics(page=page))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/file/<path:file_uid>', methods=['GET'])
def file_send(file_uid: str):
    """Отправка файлов."""
    file_path = os.path.join(
        app.config["DOLLSITE_FILE_STORAGE"],
        file_uid
    )
    if not os.path.exists(file_path):
        return abort(404, 'file "{}" does not exists'.format(file_uid))
    elif not os.path.isfile(file_path):
        return abort(404, 'path "{}" is not file'.format(file_uid))
    else:
        return send_file(file_path)


@app.route('/dbping', methods=['GET'])
def dbping():
    """Пример подключения к базе данных."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("select version()")
    ver = cur.fetchone()
    app.logger.debug(ver)
    return app.config['PROJECT_PATH']
