from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    PasswordField,
    SubmitField,
    StringField,
    EmailField,
    BooleanField
)
from wtforms.validators import DataRequired


class EmergencyAccessForm(FlaskForm):
    astronaut_id = IntegerField('id астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField(
        'Пароль астронавта', validators=[DataRequired()]
    )
    capitan_id = IntegerField('id капитана', validators=[DataRequired()])
    capitan_password = PasswordField(
        'Пароль капитана', validators=[DataRequired()]
    )
    submit = SubmitField('Доступ')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Профессия', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    password_again = StringField(
        'Повторите пароль', validators=[DataRequired()]
    )
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobCreateForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Длительность работы в часах', validators=[DataRequired()])
    collaborators = StringField('Коллабораторы', validators=[DataRequired()])
    is_finished = BooleanField('Закончена')
    team_leader = IntegerField('Глава', validators=[DataRequired()])
    submit = SubmitField('Добавить')