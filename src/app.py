"""В модуле app.py происходит создание и настройка инстанса приложения."""

from flask import Flask

app = Flask(
    __name__,
    template_folder='../build',
    static_folder='../build/static'
)
app.debug = True

app.config.from_object('config')

if __name__ == "__main__":
    app.run()
