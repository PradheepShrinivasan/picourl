from flask_wtf import Form

from wtforms import SubmitField

class LogoutForm(Form):

    submit = SubmitField('Logout')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


