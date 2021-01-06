from flask_wtf import FlaskForm

from wtforms import SubmitField


class LogoutForm(FlaskForm):
    """  Logout form for user """

    submit = SubmitField('Logout')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
