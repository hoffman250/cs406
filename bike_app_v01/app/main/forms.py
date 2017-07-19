from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, \
	IntegerField, RadioField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from flask_pagedown.fields import PageDownField


class PersonalForm(FlaskForm):
	first_name = StringField('First Name', validators=[Required()])
	last_name = StringField('Last Name', validators=[Required()])
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	phone = TelField(validators=[Required()])
	address = TextAreaField('Address', validators=[Required()])
	city = StringField('City', validators=[Required()])
	state = SelectField('State', choices = [('AK', 'Alaska'), 
      ('Al', 'Alabama')])
	zip_code = IntegerField('Zip', validators=[Required(), Length(5)])

	height = SelectField('Height', choices = [('60', '5\'0'), 
      											('61', '5\'1'),
      											('62', '5\'2'),
      											('63', '5\'3'),
      											])
	weight = IntegerField('Weight')
	submit = SubmitField('Purchase')
	skill_level = SelectField('Skill Level', choices = [('nov', 'novice'), 
      											('int', 'intermediate'),
      											('adv', 'advanced'),
      											('pro', 'professional')
      											])
	style = SelectField('Riding Style', choices = [('cruise', 'cruiser'),
													('mtn', 'mountain bike'),
													('cross', 'cycle cross'),
													('street', 'street')
													])
	gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
	dob = DateTimeField('Date of Birth', format='%m/%d/%y')
