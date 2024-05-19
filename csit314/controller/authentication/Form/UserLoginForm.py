from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class UserLoginForm(FlaskForm):
    """
    Form for user login.
    """
    userid = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])