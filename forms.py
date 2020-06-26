from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
#import email_validator
# from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    user = StringField('Username')
    password = PasswordField('Password')
