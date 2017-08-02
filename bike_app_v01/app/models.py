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

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
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

	@staticmethod     
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
					username=forgery_py.internet.user_name(True),
					password=forgery_py.lorem_ipsum.word(),
					confirmed=True,
					name=forgery_py.name.full_name())
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

	@property 
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

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

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

	def generate_email_change_token(self, new_email, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'change_email': self.id, 'new_email': new_email})

	def change_email(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('change_email') != self.id:
			return False
		new_email = data.get('new_email')
		if new_email is None:
			return False
		if self.query.filter_by(email=new_email).first() is not None:
			return False
		self.email = new_email
		self.avatar_hash = hashlib.md5(
			self.email.endcode('utf-8')).hexdigest()
		db.session.add(self)
		return True

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	def __repr__(self):
		return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

class Bike(UserMixin, db.Model):
	__tablename__ = 'bikes'
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(64), index=True)
	model = db.Column(db.String(64), index=True)
	style = db.Column(db.String(64))
	rate = db.Column(db.String(64))


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
