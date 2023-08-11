from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_test.config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError

db = SQLAlchemy()


def create_app():
    print(__name__)
    app = Flask(__name__)

    #  подключаем файл конфига
    app.config.from_object(Config)

    db.init_app(app)

    #  регистрация блюпринта main
    from flask_test.main.routes import main
    app.register_blueprint(main)

    #  регистрация buyers
    from flask_test.buyers.routes import buyers
    app.register_blueprint(buyers)

    return app

# csrf = CSRFProtect(create_app())
