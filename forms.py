from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateTimeField
from wtforms import SelectField, TextAreaField, SubmitField
#import email_validator
# from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import validators
from wtforms.validators import NumberRange, Required
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    user = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Log In')


class PatientRegisterForm(FlaskForm):
    # ssn = StringField("Patient SSN")
    patient_id = StringField("Patient ID")
    patient_name = StringField("Patient Name")
    patient_age = IntegerField('Age', validators=[Required(), NumberRange(min=1, max=99, message="Should be between 1 and 99")])
    date_of_admission = DateField("Admission date", format='%Y-%m-%d')
    type_of_bed = SelectField('Type of Bed', choices=[
        ("general word", "General Word"),
        ("semi sharing", "Semi Sharing"),
        ("single room", "Single Room")],
        validators=[Required()])
    address = TextAreaField("Address", validators=[Required()])
    state = StringField("State", validators=[Required()])
    city = StringField("City", validators=[Required()])
    status = SelectField("Status", choices=[
                         ("active", "Active"),
                         ("discharge", "Discharge")],
                         validators=[Required()])
    submit = SubmitField("Submit")


class PatientSearchForm(FlaskForm):
    patient_id = StringField("Patient ID")
    submit = SubmitField("Submit")


class patientdetailsForm(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[Required(message="Please Enter an Integer")])
    submit = SubmitField("Submit")