from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UrlForm(FlaskForm):
    '''
    '''
    neighbourhood = StringField('Neighbourhood', validators=[DataRequired])
    city = StringField('City', validators=[DataRequired])
    state = StringField('State', validators=[DataRequired])
