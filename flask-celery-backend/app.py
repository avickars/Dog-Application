import json
import os
import uuid
from functools import wraps

import boto3
import pandas as pd
import torch
from PIL import Image
from flask import Flask

from flask import request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from dog_detection_demo.extractor import dog_extractor
from dog_identification_demo.comparator import dog_comparator, sigmoid
from flask_celery import make_celery
from decouple import config
from sqlalchemy.sql.schema import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if config("AWS_ACCESS_KEY_ID", default='') != '':

    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default='')
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default='')
    REGION_NAME = config("REGION_NAME", default='')

    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='')
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default='')

else:

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    REGION_NAME = os.environ['REGION_NAME']

    CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

basedir = os.getcwd()



app = Flask(__name__)
db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app



app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def _init_(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','email','name','phone', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserSession(db.Model):
    __tablename__ = 'user_session'
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(80), unique=True, nullable=False)
    device_type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer,
                          db.ForeignKey("user.id"), nullable=False,
                          index=True)

    def _init_(self, refresh_token, user_id, device_type):
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.device_type = device_type


# JSON Schema
class UserSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'refresh_token', 'user_id', 'device_type')


user_session_schema = UserSessionSchema()
user_session_s_schema = UserSessionSchema(many=True)

class Pets(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                          db.ForeignKey("user.id"), nullable=False,
                          index=True)
    image_url = db.Column(db.String(80), nullable=False)
    is_lost = db.Column(db.Integer)
    dog_extractor = db.Column(db.JSON)
    dog_identification = db.Column(db.JSON)
    final_output = db.Column(db.JSON)


    def _init_(self, user_id, image_url, is_lost, dog_extractor, dog_identification, final_output):
        self.user_id = user_id
        self.image_url = image_url
        self.is_lost = is_lost
        self.dog_extractor = dog_extractor
        self.dog_identification = dog_identification
        self.final_output = final_output


# JSON Schema
class PetsSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'image_url', 'is_lost', 'dog_extractor', 'dog_identification')


# JSON Schema
class PetsSchemaUp(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'id', 'image_url', 'dog_identification')

pets_schema = PetsSchema()
pets_s_schema = PetsSchema(many=True)
pets_up_schema = PetsSchemaUp(many=True)

# file: proj/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, convert_unicode=True,
    pool_recycle=3600, pool_size=10)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


celery = make_celery(app,db)

@celery.task(name="main.run_models_in_background")
def run_models_in_background(img_pth, img_name, user_id, url, is_lost):
    app = create_app()
    with app.app_context():
        extractor_outputs = dog_extractor(img_pth)
        if extractor_outputs[0]['boxes'] == []:
            os.remove(img_name)
            data = {
                "status": True,
                "dog_extractor": None,
                "dog_identification": None,
                "image_url": None

            }

            return jsonify(data)
        comparator_outputs = dog_comparator(img_pth, extractor_outputs[0]['boxes'])

        if int(is_lost) == 1:
            find_status = 0
        else:
            find_status = 1

        fetch_pets = db_session.query(Pets).filter_by(is_lost=find_status)
        db_session.close()
        all_pets = pets_up_schema.dump(fetch_pets)
        stacked_compare = []
        if len(all_pets) > 0:
            for each_val in all_pets:
                comparison = sigmoid(torch.FloatTensor(comparator_outputs),
                                     torch.FloatTensor(each_val['dog_identification']))
                comparison = comparison.tolist()
                comparison = comparison[0]
                each_val['c_score'] = comparison
                del each_val['dog_identification']
                stacked_compare.append(each_val)
            similar_dogs = pd.DataFrame(stacked_compare)
            sorted_similar_dogs = similar_dogs.sort_values(by=['c_score']).head(3)
            display = sorted_similar_dogs.to_dict('records')
            os.remove(img_name)

        # DB entry after first model response
        pets = Pets(
            user_id=user_id,
            image_url=url,
            is_lost=int(is_lost),
            dog_extractor=extractor_outputs,
            dog_identification=comparator_outputs,
            final_output=stacked_compare
        )
        db_session.add(pets)
        db_session.commit()
        db_session.close()
        data = {
            "status": True,
            "stacked_comparision": stacked_compare,
            "image_url": url
        }
        return {"data" : data}

# App Models


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        _t = request.form.get('refresh_token', '')
        if _t == '':
            _r = json.loads(request.data)
            _t = _r['refresh_token']

            if 'refresh_token' not in _r:
                _error = jsonify({
                    "status": False,
                    "message": "Seems you have not signed in. Please sign-in!"
                })
                return _error
        _results = db.session.query(UserSession, User).join(UserSession).filter_by(refresh_token=_t).first()

        if len(_results) > 0:
            if _results[0].refresh_token is None:
                _error = jsonify({
                    "status": False,
                    "message": "Seems you have not signed in. Please sign-in!"
                })
                return _error

        kwargs['user_id'] = _results[0].user_id

        if _results is not None:
            return f(*args, **kwargs)
        else:
            _error = jsonify({
                "status": False,
                "message": "Seems you have not signed in. Please sign-in!"
            })
            return _error
    return decorated_func


@app.route('/upload', methods=['POST'])
# @handle_all_exceptions
@logged_in
def upload_lost_pet_image(*args, **kwargs):

    if 'user_id' not in kwargs:
        _error = jsonify({
            "status": False,
            "message": "Seems you have not signed in. Please sign-in!"
        })
        return _error

    user_id = kwargs['user_id']

    bucket = 'imagescmpt'

    image_file = request.files['image']
    img = Image.open(image_file.stream)
    img = img.convert('RGB')

    uui = str(uuid.uuid4())
    img_name = uui + '.jpg'
    cwd = os.getcwd()
    img.save(img_name)

    client = boto3.client('s3', region_name=REGION_NAME,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    client.upload_file(
        Bucket=bucket,
        Filename=img_name,
        Key=img_name
    )

    img_pth = cwd + '/' + img_name

    url = 'https://imagescmpt.s3.us-west-2.amazonaws.com/' + img_name

    data = {
        "status": True,
        "image_url": url
    }

    is_lost = request.form.get('lost', 0)
    run_models_in_background.delay(img_pth, img_name, user_id, url, is_lost)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='10.0.0.69')

#  pip freeze > requirements.txt
#  celery -A app.celery worker --loglevel=INFO