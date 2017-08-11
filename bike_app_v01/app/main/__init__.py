# main/__init__.py
# creates blueprint for main/views.py
# code courtesy of Flask Web Developement, Miguel Grinberg


from flask import Blueprint

main = Blueprint('main', __name__)
from . import views