from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, \
	TextAreaField, IntegerField, RadioField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
			'Usernames must have only letters, '
			'numbers, dots or underscores')])
	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Passwords must match!')])
	password2 = PasswordField('Confirm password', validators=[Required()])

	first_name = StringField('First Name', validators=[Required()])
	last_name = StringField('Last Name', validators=[Required()])
	phone = TelField(validators=[Required()])
	address = TextAreaField('Address', validators=[Required()])
	city = StringField('City', validators=[Required()])
	state = SelectField('State', choices = [('AK', 'Alaska'), 
      ('Al', 'Alabama')])
	zip_code = TextAreaField('Zip', validators=[Required(), Length(5)])

	height = SelectField('Height', choices = [('60', '5\'0'), 
      											('61', '5\'1'),
      											('62', '5\'2'),
      											('63', '5\'3'),
      											])
	weight = TextAreaField('Weight')
	# submit = SubmitField('Purchase')
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
	# dob = DateTimeField('Date of Birth', format='%m/%d/%y')

	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')