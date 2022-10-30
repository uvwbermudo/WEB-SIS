from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField



class AddCollege(FlaskForm):
    college_code = StringField('College Code', 
    [validators.Length(min=1, max=50), 
    validators.DataRequired(message='College Code is required'), 
    validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for College Code. (Can\'t start with spaces)')])

    college_name = StringField('College Name', 
    [validators.Length(min=1, max=50), 
    validators.DataRequired(message='College Name is required'), 
    validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for College Name. (Can\'t start with spaces)')])

    submit = SubmitField("Submit")



