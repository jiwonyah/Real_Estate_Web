from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

class UserSignUpForm(FlaskForm):
    """
    Form for user sign up.
    """
    userid = StringField('ID', validators=[
        DataRequired(),
        Length(min=5, max=25, message='ID length must be 5~25.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=25, message='Password must be 8~25.')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=8, max=25)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
        ('agent', 'Agent')
    ], validators=[DataRequired()])
    # role = SelectField('Role', choices=[
    #     (Role.SELLER.value, 'Seller'),
    #     (Role.BUYER.value, 'Buyer'),
    #     (Role.AGENT.value, 'Agent')
    # ], validators=[DataRequired()])