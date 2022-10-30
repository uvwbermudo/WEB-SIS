from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField



class AddCollege(FlaskForm):
    college_code = StringField('College Code', 
    [validators.Length(min=1, max=20), 
    validators.DataRequired(message='College Code is required'), 
    validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for College Code. (Unnecessary Spaces.)')],
    render_kw={'placeholder':"e.g. 'CCS'"})

    college_name = StringField('College Name', 
    [validators.Length(min=1, max=100), 
    validators.DataRequired(message='College Name is required'), 
    validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid Format for College Name. (Unnecessary Spaces.)')])

    submit = SubmitField("Submit")



