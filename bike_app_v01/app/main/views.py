from flask import render_template, redirect, url_for, flash, request, \
	current_app, make_response
from . import main
from .forms import PersonalForm

@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@main.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

@main.route('/browse_bikes', methods=['GET', 'POST'])
def browse_bikes():
	return render_template('browse_bikes.html')


@main.route('/participating_dealers', methods=['GET', 'POST'])
def participating_dealers():
	return render_template('participating_dealers.html')

@main.route('/faq', methods=['GET', 'POST'])
def faq():
	return render_template('faq.html')

@main.route('/purchase', methods=['GET', 'POST'])
def purchase():
	form = PersonalForm()
	return render_template('purchase.html', form=form)