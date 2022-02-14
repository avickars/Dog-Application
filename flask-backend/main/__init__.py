from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ''


db = SQLAlchemy(app)

# import and register Blueprints
from .user import user
app.register_blueprint(user, url_prefix='/auth')
