from flask import render_template, redirect, url_for, flash, request, \
	current_app, make_response
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
	
	return render_template('index.html')

@main.route('/about', methods=['GET', 'POST'])
def about():
	
	return render_template('about.html')