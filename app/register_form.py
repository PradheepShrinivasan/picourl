from flask_wtf import FlaskForm

from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import email, data_required


class RegisterForm(FlaskForm):
    """ handles all the user registration """
    email = StringField('email', validators=[email(message="Must be an email address"),
                                             data_required(message="Email address is mandatory")])
    password = PasswordField('Password',
                             validators=[data_required(message="Password is mandatory"),
                                        validators.Length(min=5, max=32, message="Password Length must be 5 to 32 char")],
                            )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[data_required(),
                                                 validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """  performs validation of input  """
        if  FlaskForm.validate(self):
            return True
        return False
