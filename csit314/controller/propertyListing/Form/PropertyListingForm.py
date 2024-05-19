from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

class PropertyListingForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    images = FileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    content = TextAreaField('Content')
    price = IntegerField('Price', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    floorSize = IntegerField('Floor Size', validators=[DataRequired()])
    floorLevel = SelectField('Floor Level', choices=[
        (FloorLevel.LOW.value, 'Low'),
        (FloorLevel.MEDIUM.value, 'Medium'),
        (FloorLevel.HIGH.value, 'High')
    ], validators=[DataRequired()])
    propertyType = SelectField('Property Type', choices=[
        (PropertyType.HDB.value, 'HDB'),
        (PropertyType.CONDO.value, 'Condo'),
        (PropertyType.APARTMENT.value, 'Apartment'),
        (PropertyType.STUDIO.value, 'Studio')
    ], validators=[DataRequired()])
    furnishing = SelectField('Furnishing', choices=[
        (Furnishing.PartiallyFurnished.value, 'Partially furnished'),
        (Furnishing.FullyFurnished.value, 'Fully furnished'),
        (Furnishing.NotFurnished.value, 'Not furnished')
    ], validators=[DataRequired()])
    builtYear = IntegerField('Built Year', validators=[DataRequired()])
    client_id = StringField('Client',  validators=[DataRequired()])
    is_sold = BooleanField('Is Sold')