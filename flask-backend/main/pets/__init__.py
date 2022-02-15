from flask import Blueprint

pets = Blueprint('pets', __name__)

from . import views