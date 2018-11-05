"""Модуль содержит правила роутинга приложения."""

from functools import wraps
import os

from app import app
from db import get_db
from flask import (
    abort,
    jsonify,
    make_response,
    request,
    send_file,
)
from json_methods import collections_bublics, get_lot
from models import Merch


def _access_control_allow_origin(func):
    @wraps(func)
    def wrap(*arg, **kw):
        response = func(*arg, **kw)
        response = make_response(response)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrap


@app.route('/lot', methods=['GET'])
@_access_control_allow_origin
def lot():
    """Информация о лотах."""
    lot_id = request.args.get('lot_id', None)
    return jsonify(get_lot(lot_id))


@app.route('/collections/bublics', methods=['GET'])
@_access_control_allow_origin
def bublics():
    """Информация о бубликах."""
    page = request.args.get('page', None)
    app.logger.debug(collections_bublics(page=page))
    return jsonify(collections_bublics(page=page))


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


@app.route('/merch/insert', methods=['POST'])
@_access_control_allow_origin
def merch_insert():
    """Метод API добавления товара."""
    merch_uuid = request.form.get('uuid', None)
    merch_name = request.form.get('name', '')
    merch_desc = request.form.get('desc', '')

    if not merch_name and not merch_desc:
        return abort(404, 'No data')

    merch = Merch(name=merch_name, desc=merch_desc, uuid=merch_uuid)
    merch.insert()

    return merch.uuid


@app.route('/merch/update', methods=['POST'])
@_access_control_allow_origin
def merch_update():
    """Метод API изменения товара."""
    merch_uuid = request.form['uuid']

    merch = Merch.by_uuid(merch_uuid)
    if merch is None:
        return abort(404, "Merch '{}' doesn't find".format(merch_uuid))

    merch.name = request.form.get('name', merch.name)
    merch.desc = request.form.get('desc', merch.desc)
    merch.update()

    return 'OK'


@app.route('/merch/delete', methods=['POST'])
@_access_control_allow_origin
def merch_delete():
    """Метод API удаления товара."""
    app.logger.debug(request.form)
    merch_uuid = request.form['uuid']

    merch = Merch.by_uuid(merch_uuid)
    if merch:
        merch.delete()
    return 'OK'


@app.route('/merch/lst', methods=['POST'])
@_access_control_allow_origin
def merch_lst():
    """Метод API для получения списка товаров."""
    res = []
    for merch in Merch.lst():
        res.append({
            "uuid": merch.uuid,
            "name": merch.name,
            "desc": merch.desc
        })
    return jsonify(res)


@app.route('/dbping', methods=['GET'])
@_access_control_allow_origin
def dbping():
    """Пример подключения к базе данных."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("select version()")
    ver = cur.fetchone()
    app.logger.debug(ver)
    return app.config['PROJECT_PATH']
