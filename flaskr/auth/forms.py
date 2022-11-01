from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo



class UserForm(FlaskForm):
    email = StringField(
        'Email Address', 
        validators=[
            Length(min=10, max=50),
            Email(message='Please enter a valid Email'),
            DataRequired()
            ],
        )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Please enter a password')
            ],
        )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address', 
        validators=[
            Length(min=10, max=50), 
            Email(message='Invalid Email'),
            DataRequired()
            ],
        )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            EqualTo('password2', message='Passwords must match')
            ]
        )
    password2 = PasswordField(
        'Confirm Password', 
        validators=[
            validators.DataRequired(),
            EqualTo('password', message='Passwords must match')
            ]
        )
    submit = SubmitField("Register")


