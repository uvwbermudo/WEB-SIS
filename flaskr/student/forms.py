from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField



class AddStudent(FlaskForm):
    id = StringField('ID Number', 
    [validators.Length(min=9, max=9, message='Must be exactly 9 characters. (e.g. "2020-1971")'), 
    validators.DataRequired(message='ID Number is required'), 
    validators.Regexp('\A([0-9]{4})-([0-9]{4})\Z', message='Cannot Submit, Invalid format for ID Number. (e.g. "2020-1971")')], 
    render_kw={'placeholder':"e.g. '2020-1971'"})

    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired(message='First name is Required'), validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid format for First Name. (Unnecessary Spaces)')])

    last_name = StringField('Last Name', [validators.Length(min=1, max=50), 
    validators.DataRequired(message='Last name is Required'), validators.Regexp('\A\w+( \w+)*\Z', message='Cannot Submit, Invalid format for Last Name. (Unnecessary Spaces)')])

    year = SelectField('Year Level', choices=[1,2,3,4,5])

    gender = SelectField('Gender', choices = ['Male','Female'])

    course = SelectField('Course')

    
    submit = SubmitField("Submit")





