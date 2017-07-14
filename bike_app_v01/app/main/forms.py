from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField 
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
	body = PageDownField("What you thinkin?", validators=[Required()])
	submit = SubmitField("Submit")
