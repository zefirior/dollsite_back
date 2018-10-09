"""
Входная точка приложения.

Содержит инстанс приложения.
Импортирует модули с логикой.
"""

from app import app

import db  # noqa
import route  # noqa

if __name__ == "__main__":
    app.run()
