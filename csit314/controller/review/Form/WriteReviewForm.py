from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, HiddenField, RadioField, SubmitField

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    content = TextAreaField('Content',
                            validators=[DataRequired('Content is a mandatory field')],
                            render_kw={"placeholder": "Please write review"})
    submit = SubmitField('Submit Review')