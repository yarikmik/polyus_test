from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length


class AddProductsForm(FlaskForm):
    product_name = StringField('Наименование товара:', validators=[DataRequired(), Length(min=2, max=20)])
    purchase_cost = FloatField('Цена закупки:')
    selling_cost = FloatField('Цена продажи:')
    submit = SubmitField('Подтвердить')
