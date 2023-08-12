from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_test.config import Config

db = SQLAlchemy()


def create_app():
    print(__name__)
    app = Flask(__name__)

    with app.app_context():
        #  подключаем файл конфига
        app.config.from_object(Config)

        db.init_app(app)

        #  регистрация блюпринта main
        from flask_test.main.routes import main
        app.register_blueprint(main)

        #  регистрация buyers
        from flask_test.buyers.routes import buyers
        app.register_blueprint(buyers)

        #  регистрация products
        from flask_test.products.routes import products
        app.register_blueprint(products)

        #  регистрация purchases
        from flask_test.purchases.routes import purchases
        app.register_blueprint(purchases)

        #  регистрация report
        from flask_test.report.routes import report
        app.register_blueprint(report)

        return app
