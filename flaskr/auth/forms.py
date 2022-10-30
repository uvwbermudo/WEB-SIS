from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField



class UserForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=10, max=50), validators.Email(message='Please enter a valid Email'),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(message='Please enter a password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=10, max=50), validators.Email(message='Invalid Email'),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField("Register")


