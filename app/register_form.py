from flask_wtf import Form

from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import email, data_required


class RegisterForm(Form):
    """ handles all the user registration """
    email = StringField('email', validators=[email(), data_required()])
    password = PasswordField('Password', validators=[data_required()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[data_required(),validators.Length(min=5, max=32),
                                                 validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """  performs validation of input  """
        if  Form.validate(self):
            return True
        return False
