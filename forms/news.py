from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

# Форма создания нового товара со всеми необходимыми полями
class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    cost = TextAreaField("Цена")
    contet = TextAreaField("Фотография")
    submit = SubmitField('Применить')