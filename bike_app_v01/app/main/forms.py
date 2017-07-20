from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, \
	IntegerField, RadioField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from flask_pagedown.fields import PageDownField


class PurchaseForm(FlaskForm):
	first_name = StringField('First Name', validators=[Required()])
	last_name = StringField('Last Name', validators=[Required()])
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	phone = TelField(validators=[Required()])
	address = TextAreaField('Address', validators=[Required()])
	city = StringField('City', validators=[Required()])
	state = SelectField('State', choices = [('AK', 'Alaska'), 
      ('Al', 'Alabama')])
	zip_code = IntegerField('Zip', validators=[Required(), Length(5)])
