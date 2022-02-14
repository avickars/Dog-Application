from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@database-1.cabcbf9wyrc1.us-west-2.rds.amazonaws.com:5432/dogfinder'


db = SQLAlchemy(app)
ma = Marshmallow(app)

# import and register Blueprints
from .user import user
app.register_blueprint(user, url_prefix='/auth')
