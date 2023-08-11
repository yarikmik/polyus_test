from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_test import db
from flask_test.models import Buyers, Products
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


def get_userdata():
    return db.session.query(Buyers).all()


class AddPurchasesForm(FlaskForm):
    purchase_date = DateField('Дата продажи:', format='%Y-%m-%d')
    buyer_name = QuerySelectField('Покупатель', query_factory=get_userdata,
                                  get_label="username")
    purchase_name = QuerySelectField('Продукт:', query_factory=lambda: db.session.query(Products).all(),
                                     get_label="product_name")
    count = FloatField('Количество:')
    unit_cost = FloatField('Стоимость за единицу:')
    total_cost = FloatField('Сумма:')
    submit = SubmitField('Подтвердить')

    # choices=[(u.username, u.username) for u in Buyers.query.all()]
