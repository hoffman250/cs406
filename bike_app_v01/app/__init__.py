# app/__init__.py
# file creates an application instance of Flask
# code courtesy of Flask Web Developement, Miguel Grinberg

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_pagedown import PageDown

# initializing Flask extensions
bootstrap = Bootstrap()		
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# instantiating a Flask object, using Flask 'application factory'
def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)

	# blueprint setup for main/views.py
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	# blueprint setup for auth/views.py
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	return app 
