"""Конфиги."""

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
DOLLSITE_FILE_STORAGE = os.getenv('DOLLSITE_FILE_STORAGE', PROJECT_PATH)

DS_DB_PASSW = os.getenv("DS_DB_PASSW")
