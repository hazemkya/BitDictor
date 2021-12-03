from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class prediction_Input(FlaskForm):
    days_to_predict = IntegerField('Days to predict', validators=[
                                   NumberRange(min=1, max=100), DataRequired()])
    submit = SubmitField('Predict')
