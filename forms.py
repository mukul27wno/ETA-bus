from flask_wtf import FlaskForm #wt forms
from wtforms import StringField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired 

class AddTaskForm(FlaskForm):
    per_route = IntegerField('', validators=[DataRequired()])
    curr_time = StringField('Number of Tweets - ')
    submit = SubmitField('Submit')