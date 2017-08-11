# auth/__init__.py
# creates blueprint for auth/views.py
# code courtesy of Flask Web Developement, Miguel Grinberg


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views