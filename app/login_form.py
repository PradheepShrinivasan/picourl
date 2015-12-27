from flask import flash
from flask_wtf import Form

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import email, data_required


from user import User

class LoginForm(Form):

    email = StringField('email', validators=[email(), data_required()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login')
    register = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


    def validate(self):
        """checks the validity of the form data and also compares
            it with the password from database to make sure that
            its valid"""
        if not Form.validate(self):
            return False

        user = User.getuser(self.email.data.lower())
        if user and user.checkpassword(self.password.data):
            flash("Login successful")
            return True
        else:
            flash("Invalid e-mail or password")
            return False


