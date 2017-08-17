# config.py
# file contains configuration data for program
# code structure courtesy of Flask Web Developement, Miguel Grinberg, modified as needed


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

	# constants
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'Marc should listen to the Devin Townsend Project'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmx.com'	# email account program sends from
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')		# function imports mail username 
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')		# function imports mail password
	MAIL_SUBJECT_PREFIX = '[Bike Demo App]'				# contant for email subject
	MAIL_SENDER = 'Admin <hoffmbri@gmx.com>'			# constant for email sender
	ADMIN = os.environ.get('ADMIN')						# placeholder for admin functionality

	# initializing init with app object
	@staticmethod
	def init_app(app):
		pass

# deveopment configuration
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

# test configuration
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

# production congiguration
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}