from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)

	#routes
	@app.route('/', methods=['GET', 'POST'])
	def index():
		form = NameForm()
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.name.data).first()
			if user is None:
				user = User(username = form.name.data)
				db.session.add(user)
				session['known'] = False
				if app.config['FLASKY_ADMIN']:
					send_email(app.config['FLASKY_ADMIN'], 'New User',
	            	'mail/new_user', user=user)
			else:
				session['known'] = True
			session['name'] = form.name.data
			form.name.data = ''
			return redirect(url_for('index'))
		return render_template('index.html', form=form, name=session.get('name'), 
			known = session.get('known', False),
			current_time=datetime.utcnow())

	@app.route('/user/<name>')
	def user(name):
	    return render_template('user.html', name=name)

	@app.errorhandler(404)
	def page_not_found(e):
	    return render_template('404.html'), 404

	@app.errorhandler(500)
	def internal_server_error(e):
	    return render_template('500.html'), 500

	if __name__ == '__main__':
		# db.create_all()
		manager.run()

	return app 