from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SubmitField
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
