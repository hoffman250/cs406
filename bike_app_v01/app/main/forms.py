from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField 
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class PurchaseForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	submit = SubmitField('Purchase')
