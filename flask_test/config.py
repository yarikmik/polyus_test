import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/database.sqlite3')
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
