# models.py
# file contains models for User, Bike and Purchase tables in the database
# File structure based on model.py in Flask Web Developement, Miguel Grinberg

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from markdown import markdown
import bleach
import hashlib

# User table
# creates table to hold user attributes
class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))	# stores password hash
	confirmed = db.Column(db.Boolean, default=False)
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	phone = db.Column(db.Integer)
	address = db.Column(db.String(64), unique=True)
	city = db.Column(db.String(64))
	state = db.Column(db.String(64))
	zip_code = db.Column(db.String(64))
	height = db.Column(db.String(64))
	weight = db.Column(db.String(64))
	skill_level = db.Column(db.String(64))
	style = db.Column(db.String(64))
	gender = db.Column(db.String(64))

	# returns error is hashed password is read
	@property 
	def password(self):
		raise AttributeError('password is not a readable attribute')

	# password generate function from Werkzeug
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	# Werkzeug function checks entered password against stored hashed password in User table
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# itsdangerous function generates confirmation token for registration
	# uses secret key constant from config.py
	# expires in 3600 seconds
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	# itsdangerous function verifies token
	# if verified, sets 'confirmed' to true indicating user is authenticated
	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	# ping function used in auth/views.py, checks user confirmation status
	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	# provides string output of class (used for debug)
	def __repr__(self):
		return '<User %r>' % self.username

# Bike table
# creates table to hold bike attributes
class Bike(UserMixin, db.Model):
	__tablename__ = 'bikes'
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(64), index=True)
	model = db.Column(db.String(64), index=True)
	style = db.Column(db.String(64))
	rate = db.Column(db.String(64))

# Purchase table
# creates table to hold purchase transaction attributes
class Purchase(UserMixin, db.Model):
	__tablename__ = 'purchases'
	id = db.Column(db.Integer, primary_key=True)
	credit_card = db.Column(db.String(64), index=True)
	credit_card_number = db.Column(db.String(64), index=True)
	ccv = db.Column(db.String(64))

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

login_manager.anonymous_user = AnonymousUser

# function queries User table, returns user's id 
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
