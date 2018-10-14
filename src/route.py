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
    app.logger.debug(collections_bublics(page=page))
    response = jsonify(collections_bublics(page=page))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/file/<uuid:file_uuid>', methods=['GET'])
def file_send(file_uuid):
    """Отправка файлов."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "select file_path from source_file where code = %s",
        (str(file_uuid), )
    )
    file_name = cur.fetchone()
    if file_name is None:
        return abort(404, 'File does not exists')
    else:
        file_name = file_name[0]

    file_path = os.path.join(
        app.config["DOLLSITE_FILE_STORAGE"],
        file_name
    )

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return abort(404, 'File does not exists')

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
