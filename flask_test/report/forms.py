from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField


class SelectDateFrom(FlaskForm):
    date_from = DateField('Отчет с даты:', format='%Y-%m-%d')
    submit = SubmitField('Подтвердить')
