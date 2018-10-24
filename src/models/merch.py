"""Модуль. Модель 'Товар'."""

import uuid

from app import app
import attr
from db import db_cursor


@attr.s
class Merch:
    """Модель 'Товар'."""

    name = attr.ib(converter=str)
    desc = attr.ib(converter=str)
    _uuid = attr.ib(default=None)

    @property
    def uuid(self):
        """UUID товара."""
        return self._uuid

    @classmethod
    def by_uuid(cls, uuid):
        """Метод возвращает инстанс 'Товар' по его UUID."""
        with db_cursor() as cur:
            cur.execute(
                """
                SELECT uuid, name, description
                FROM merch
                WHERE uuid = %s
                """,
                (str(uuid), )
            )
            app.logger.info(cur.query)

            res = cur.fetchone()

        if res:
            uuid, name, desc = res
            return cls(name, desc, uuid)

    def _generate_uuid(self):
        self._uuid = str(uuid.uuid4())

    def _insert(self):
        self._generate_uuid()
        with db_cursor() as cur:
            cur.execute(
                """
                INSERT INTO merch (uuid, name, description)
                VALUES (%s, %s, %s)
                """,
                (self._uuid, self.name, self.desc)
            )
            app.logger.info(cur.query)
            cur.connection.commit()

    def _update(self):
        with db_cursor() as cur:
            cur.execute(
                """
                UPDATE merch
                SET name = %s, description = %s
                WHERE uuid = %s
                """,
                (self.name, self.desc, self._uuid)
            )
            app.logger.info(cur.query)
            cur.connection.commit()

    def update(self):
        """Запись данных в базу."""
        if self._uuid is None:
            self._insert()
        else:
            self._update()
