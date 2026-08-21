from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL


class CafeForm(FlaskForm):
    """Form for adding a new cafe. Demonstrates advanced Flask-WTF fields:
    URLField (built-in URL input type) and SelectField (dropdown)."""

    cafe = StringField('Cafe name', validators=[DataRequired()])

    location = URLField(
        'Cafe Location on Google Maps (URL)',
        validators=[DataRequired(), URL(message="Please enter a valid URL.")]
    )

    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])

    coffee_rating = SelectField(
        'Coffee Rating',
        choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'],
        validators=[DataRequired()]
    )

    wifi_rating = SelectField(
        'Wifi Strength Rating',
        choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
        validators=[DataRequired()]
    )

    power_rating = SelectField(
        'Power Socket Availability',
        choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit')