# auth/views.py
# file contains routes for 'authorizing' user login & registration


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

# function to check that user has confirmed their registration
@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
				and request.endpoint \
				and request.endpoint[:5] != 'auth.' \
				and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))

# route to deal with unconfirmed user
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))	# if the user actually is confirmed, send to index
	return render_template('auth/unconfirmed.html')

# route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

# route to log user out, return to index
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

# route to register user
# creates a user object, stores user attributes in user table
# sends a confirmation email to user upon registration attempt 
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data,
					first_name=form.first_name.data,
					last_name=form.last_name.data,
					phone=form.phone.data,
					address=form.address.data,
					city=form.city.data,
					state=form.state.data,
					zip_code=form.zip_code.data,
					height=form.height.data,
					weight=form.weight.data,
					skill_level=form.skill_level.data,
					style=form.style.data,
					gender=form.gender.data
					)
		db.session.add(user)	# add user to database
		db.session.commit()		# commit this update to database
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm your account', 'auth/email/confirm',
			user=user, token=token)
		flash('A confirmation email will be sent to you')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

# route for when user clicks link in confirmation email
# confirms token that was sent in email
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Dankeschoen.')
	else:
		flash('The confirmation link is invalid or expired.')
	return redirect(url_for('main.index'))
