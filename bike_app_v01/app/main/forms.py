from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, \
	IntegerField, RadioField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from flask_pagedown.fields import PageDownField


class PurchaseForm(FlaskForm):
	credit_card = SelectField('Credit Card Type', choices = [('visa', 'Visa'), 
      ('mastercard', 'Master Card'), ('amex', 'American Express')])
	credit_card_number = StringField('Credit Card Number', validators=[
		Required(), Length(16), Regexp('^[0-9]*$', 0,
			'Credit card number must only contain numbers')])
	ccv = StringField('CCV Number', validators=[
		Required(), Length(3), Regexp('^[0-9]*$', 0,
			'CCV must only contain numbers')])
	submit = SubmitField('Purchase')
