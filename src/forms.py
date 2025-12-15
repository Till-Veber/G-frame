from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models.user import User

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(min=3, max=20)
    ])
    email = EmailField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(), Length(min=6)
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли должны совпадать.')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким email уже существует.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')