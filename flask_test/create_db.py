from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)


class Buyers(db.Model):
    """модель покупателей"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    year_of_birth = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.Enum('Man', 'Woman', 'Unknown'), name='Gender', default='Unknown')
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    consent = db.Column(db.Boolean, default=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')


class Products(db.Model):
    """модель товаров"""
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), unique=True, nullable=False)
    purchase_cost = db.Column(db.Float)
    selling_cost = db.Column(db.Float)


class Purchases(db.Model):
    """модель покупок"""
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    count = db.Column(db.Integer)
    unit_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)


with app.app_context():
    db.create_all()
