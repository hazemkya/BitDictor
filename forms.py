from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError

def int_check(form, field):
    if type(field.data) != type(int):
        raise ValidationError('Number must be an integer')

class prediction(FlaskForm):
    days_to_predict = IntegerField('Days to predict', validators=[NumberRange(min=1, max= 10), DataRequired()])
    submit = SubmitField('Predict')


