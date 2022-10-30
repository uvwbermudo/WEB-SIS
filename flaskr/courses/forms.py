from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField



class AddCourse(FlaskForm):
    course_code = StringField('Course Code', 
    [validators.Length(min=1, max=50), 
    validators.DataRequired(message='Course Code is required'), validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid format for Course Code. (Can\'t start with spaces)')])

    course_name = StringField('Course Name',
    [validators.Length(min=1, max=50), 
    validators.DataRequired(message='Course Name is required'),
     validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for Course Name. (Can\'t start with spaces)')])

    college = SelectField('College Origin', [validators.Length(min=2, max=50), validators.DataRequired()])

    submit = SubmitField("Submit")



