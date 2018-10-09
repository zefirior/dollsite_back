"""Временный модуль, переписать на выборки из базы."""

import json
import os

from config import PROJECT_PATH


def get_lot(lot_id=None):
    """Информация о лоте из файла "jsons/lot.json"."""
    file_path = os.path.join(PROJECT_PATH, 'jsons/lot.json')
    with open(file_path) as jf:
        data = json.load(jf)
    if lot_id:
        data = [lot for lot in data if lot['id'] == int(lot_id)]
    return data


def collections_bublics(page=None):
    """Информация о бубликах из файла "jsons/collections/bublics.json"."""
    page_size = 10
    page = page or 1

    def check_page(num):
        from_ = (page - 1) * page_size + 1
        to_ = from_ + page_size
        return from_ <= num < to_

    file_path = os.path.join(PROJECT_PATH, 'jsons/collections/bublics.json')
    with open(file_path) as jf:
        data = json.load(jf)
        data = [product for product in data if check_page(product['id'])]
    return data


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_lot())
