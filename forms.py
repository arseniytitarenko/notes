from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired


class AddArticle(FlaskForm):
    title = StringField('Название статьи', validators=[InputRequired()])
    author = StringField('Автор', validators=[InputRequired()])
    date = DateField('Дата создания', validators=[InputRequired()])
    source = StringField('Источник статьи', validators=[InputRequired()])
    content = TextAreaField('Текст статьи', validators=[InputRequired()])
    submit = SubmitField('Добавить статью')

class EditArticle(FlaskForm):
    title = StringField('Название статьи', validators=[InputRequired()])
    author = StringField('Автор', validators=[InputRequired()])
    date = DateField('Дата создания', validators=[InputRequired()])
    source = StringField('Источник статьи', validators=[InputRequired()])
    content = TextAreaField('Текст статьи', validators=[InputRequired()])
    submit = SubmitField('Изменить статью')