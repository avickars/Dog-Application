from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from decouple import config

import os

basedir = os.getcwd()

if config("SQLALCHEMY_DATABASE_URI", default='') != '':
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default='')
    SEND_GRID_API_KEY = config('SEND_GRID_API_KEY', default='')

else:
    # Done
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SEND_GRID_API_KEY = os.environ['SEND_GRID_API_KEY']

basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SEND_GRID_API_KEY'] = SEND_GRID_API_KEY


db = SQLAlchemy(app)
ma = Marshmallow(app)

V1 = "/v1"

# import and register Blueprints
from .user import user
app.register_blueprint(user, url_prefix=f"{V1}/auth")


# import and register Blueprints
from .pets import pets
app.register_blueprint(pets, url_prefix=f"{V1}/pets")
