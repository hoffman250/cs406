from flask_wtf import Form
from wtforms import Stringfield, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email

class LoginForm(Form):
	email = Stringfield('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')