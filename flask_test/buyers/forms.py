from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length


class AddBuyersForm(FlaskForm):
    username = StringField('ФИО пользователя:', validators=[DataRequired(), Length(min=2, max=20)])
    year_of_birth = DateField('Год рождения:', format='%Y-%m-%d')
    gender = SelectField('Пол', choices=[('Man', 'Man'), ('Woman', 'Woman'), ('Unknown', 'Unknown')])
    registration_date = DateField('Дата регистрации:', format='%Y-%m-%d')
    consent = BooleanField('Согласие на обработку ПД')
    image_file = FileField('Фото:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Подтвердить')
