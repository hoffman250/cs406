# main/views.py
# file contains routes for all pages other than login & registration


from flask import render_template, redirect, url_for, flash, request, \
	current_app, make_response
from . import main
from .forms import PurchaseForm, BikeForm
from ..models import Bike, Purchase, User
from .. import db
from ..email import send_email
from flask_login import current_user


# program welcome/home/main/index page
@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

# route for about page
@main.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

# route for browse_bikes
# queries database for all bikes, passes bike object to html page
@main.route('/browse_bikes', methods=['GET', 'POST'])
def browse_bikes():
	bike = Bike.query.all()
	return render_template('browse_bikes.html', bike=bike)

# route for showing links to dealer partners
@main.route('/participating_dealers', methods=['GET', 'POST'])
def participating_dealers():
	return render_template('participating_dealers.html')

# route for faq page
@main.route('/faq', methods=['GET', 'POST'])
def faq():
	return render_template('faq.html')

# route for purchase page
# passes bike_id with path variable so that it's available on confirmation page
@main.route('/purchase/<bike_id>', methods=['GET', 'POST'])
def purchase(bike_id):
	form = PurchaseForm()
	bike_selected = Bike.query.filter_by(id=bike_id).first()
	user_email = current_user.email
	if form.validate_on_submit():
		flash('A confirmation email will be sent to you')
		purchase = Purchase(credit_card = form.credit_card.data,
							credit_card_number = form.credit_card_number.data,
							ccv = form.ccv.data
							)
		db.session.add(purchase)
		db.session.commit()
		send_email(user_email, 'Thanks for your reservation!', 'auth/email/purchase',
			user_email=user_email, bike_selected=bike_selected, form=form)
		return redirect(url_for('main.order_confirmation'))
	return render_template('purchase.html', bike_selected=bike_selected, form=form)

# route for order confirmation, shows bike that was selected
@main.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
	return render_template('order_confirmation.html')

# route to add a bike to database
@main.route('/add_bike', methods=['GET', 'POST'])
def register():
	form = BikeForm()
	if form.validate_on_submit():
		bike = Bike(brand = form.brand.data,
					model = form.model.data,
					style = form.style.data,
					rate = form.rate.data,
					)
		db.session.add(bike)
		db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('add_bike.html', form=form)