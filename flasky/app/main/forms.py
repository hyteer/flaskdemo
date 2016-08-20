from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

######## Form Class #########
class NameForm(Form):
    name = StringField('What is your anme?',validators=[DataRequired()])
    submit = SubmitField('Submit')


