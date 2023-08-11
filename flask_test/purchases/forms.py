from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_test import db
from flask_test.models import Buyers, Products
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class AddPurchasesForm(FlaskForm):
    purchase_date = DateField('Дата продажи:', format='%Y-%m-%d')
    buyer_name = SelectField('Покупатель',
                             choices=[(u.username, u.username) for u in db.session.query(Buyers).all()])
    product_name = SelectField('Продукт:',
                               choices=[(p.product_name, p.product_name) for p in db.session.query(Products).all()])
    count = FloatField('Количество:')
    unit_cost = FloatField('Стоимость за единицу:')
    total_cost = FloatField('Сумма:')
    submit = SubmitField('Подтвердить')

