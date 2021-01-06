
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import url, data_required


class ShortURLForm(FlaskForm):

    url = StringField('url', validators=[url(message="Must be valid url"),
                                         data_required(message="Url is mandatory")])
    submit = SubmitField('Shorten')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """  performs validation of input  """
        if FlaskForm.validate(self):
            return True
        return False
