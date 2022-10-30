from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField



class AddCourse(FlaskForm):
    course_code = StringField('Course Code', 
    [validators.Length(min=1, max=20), 
    validators.DataRequired(message='Course Code is required'), validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid format for Course Code. (Unnecessary Space)')],
    render_kw={'placeholder':"e.g. 'BSCS'"})

    course_name = StringField('Course Name',
    [validators.Length(min=1, max=100), 
    validators.DataRequired(message='Course Name is required'),
     validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for Course Name. (Unnecessary Space)')])

    college = SelectField('College Origin', [validators.DataRequired()])

    submit = SubmitField("Submit")



