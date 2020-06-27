from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateTimeField, SelectField, TextAreaField, SubmitField
import email_validator
from wtforms.validators import DataRequired, Length, NumberRange, Required, Regexp
from wtforms import validators
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired(), Length(min=8, max=20, message='Enter Username between 8 and 20 characters')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10, message='Enter 4 to 10 characters only'), Regexp("^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", message='Enter atleast 1 special character, 1 Number, 1 Uppercase')])
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