from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class UrlForm(FlaskForm):
    '''
    '''
    ptype = StringField('PType', validators=[DataRequired])
    place = StringField('Place', validators=[DataRequired])
    state = StringField('State', validators=[DataRequired])
