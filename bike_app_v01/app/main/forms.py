# main/forms.py
# file contains classes that build forms for user payment information and
# bike attributes


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from flask_pagedown.fields import PageDownField
from ..models import Bike

# purchase form 
# fields for user payment information
class PurchaseForm(FlaskForm):
	credit_card = SelectField('Credit Card Type', choices = [('visa', 'Visa'), 
      ('mastercard', 'Master Card'), ('amex', 'American Express')])
	credit_card_number = StringField('Credit Card Number', validators=[
		DataRequired()])
	ccv = StringField('CCV Number', validators=[
		DataRequired()])
	submit = SubmitField('Purchase')

# bike information form 
# fields for bike attributes
class BikeForm(FlaskForm):
	brand = StringField('Brand', validators=[
		DataRequired()])
	model = StringField('Model', validators=[
		DataRequired()])
	style = SelectField('Style', choices = [('Mountain', 'mtn'), 
      ('Road', 'road'), ('Cruise', 'cruiser')])
	rate = StringField('Rate', validators=[
		DataRequired()])
	submit = SubmitField('Add Bike')
