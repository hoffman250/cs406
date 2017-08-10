# email.py
# file contains functions to send email
# email functions courtesy of Flask Web Developement, Miguel Grinberg

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

# moves email to background thread to prevent blocking
def send_async_email(app, msg):
   	with app.app_context():
   	    mail.send(msg)

# send email function
# takes send to address, subject, email template, & keyword argurments
def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, 
		sender=app.config['MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr