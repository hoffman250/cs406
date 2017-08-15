# manage.py
# file contains code for command line access and unit testing functionality


#!/user/bin/env python
import os
from app import create_app, db
from app.models import User, Bike, Purchase
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Bike=Bike, Purchase=Purchase)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command 

# function for unit testing
def test():
	"""Start Unit Testing!"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()