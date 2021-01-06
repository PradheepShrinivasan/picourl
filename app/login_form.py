from flask import flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import data_required, email

from app.user import User


class LoginForm(FlaskForm):
    """" Login form to log in a user with validations """

    email = StringField('email', validators=[email(message="must be an email address"), data_required(message="No email provided")])
    password = PasswordField('Password', validators=[data_required(message="No password provided")])
    submit = SubmitField('Login')
    register = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """checks the validity of the form data and also compares
            it with the password from database to make sure that
            its valid"""
        if not FlaskForm.validate(self):
            return False

        user = User.getuser(self.email.data.lower())
        if user and user.checkpassword(self.password.data):
            return True
        else:
            flash("Invalid e-mail or password")
            return False
