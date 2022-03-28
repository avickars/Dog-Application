import json
import os
import uuid
from functools import wraps

import boto3
import pandas as pd
import torch
from PIL import Image
from flask import Flask

from flask import request, jsonify, render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from dog_detection_demo.extractor import dog_extractor
from breed_classifier.breed_detector import predict_breed
from dog_identification_demo.comparator import dog_comparator, sigmoid
from flask_celery import make_celery
from decouple import config
import requests
from sqlalchemy.sql.schema import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fcm_token = db.Column(db.String(300), nullable=False)

    def _init_(self, email,  password, fcm_token):
        self.email = email
        self.password = password
        self.fcm_token = fcm_token

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','email', 'password')

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
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    breed = db.Column(db.String(80), nullable=False)
    contact_email = db.Column(db.String(80))


    def _init_(self, user_id, image_url, is_lost, dog_extractor, dog_identification, final_output, lat, lng, breed, contact_email):
        self.user_id = user_id
        self.image_url = image_url
        self.is_lost = is_lost
        self.dog_extractor = dog_extractor
        self.dog_identification = dog_identification
        self.final_output = final_output
        self.lat = lat
        self.lng = lng
        self.breed = breed
        self.contact_email = contact_email


# JSON Schema
class PetsSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'image_url', 'is_lost', 'dog_extractor', 'breed' 'dog_identification')


# JSON Schema
class PetsSchemaUp(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'id', 'image_url', 'dog_identification', 'breed', 'lat', 'lng')

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


def format_data_for_email_temp(data=[]):
    md = []
    i = 0
    for d in data:
        idx = data.index(d)
        if i % 2 == 0:
            dn = []
        if len(dn) < 3:
            dn.append(d)
        if len(dn) == 2 or idx == (len(data) - 1):
            md.append(dn)
        i += 1
    return md


@app.route('/viewTemp')
def viewTemp():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'email_data.json')
    data = json.load(open(json_url))

    _d = format_data_for_email_temp(data)

    _message_body = {
        "title": "Here is a good news for you!",
        "message": "We found 3 match results of your lost dog.",
        "banner_img": "https://i.imgur.com/jcP2YnQ.png",
        "input_img": "https://i.imgur.com/0F2598w.png",
        "matched_results": _d
    }
    return render_template('email_template.html', **_message_body)

def send_email_to_user(data=[], to_email='karthiksrinath24007@gmail.com', count=0, uploaded_img=''):
    API_KEY = config('SEND_GRID_API_KEY', default='')
    if API_KEY == '':
        API_KEY = os.environ['SEND_GRID_API_KEY']

    _d = format_data_for_email_temp(data)

    _message_body = {
        "title": "Here is a good news for you!",
        "message": f"We found {count} match results of your lost dog.",
        "banner_img": "https://i.imgur.com/jcP2YnQ.png",
        "input_img": uploaded_img,
        "matched_results": _d
    }

    message = Mail(
        from_email='cmpt733dogapp@gmail.com',
        to_emails=to_email,
        subject='Your Dog Status',
        html_content=render_template('email_template.html', **_message_body),
        is_multiple=True
    )
    try:
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)

        if response.status_code == 202:
            return 'Email Sent'
        else:
            return 'Not able to send email'
    except Exception as e:
        return 'Not able to send email'

def sendNotificationToLostDogUser(user_id, db_session, count, ac_img, mat_img):

    _res = db_session.query(User.id, User.fcm_token).filter_by(id=user_id).first()
    db_session.close()

    if _res is not None:
        fcm_token = _res[1]
        _headers = {
            "Content-Type": "application/json",
            'Authorization': "key=AAAAM9hqUJ4:APA91bGuUaPEC6EcsTZBBCcQD29CZ-tG9dSx0rXsklvB_DZSXr6HX4Q9EkNJYW-1BHLoLVijWE8sSE8AM9S8am0KU0tnHofU5v0a57_nmQyOR_6ybl_ZqEXGu94m5Dv6igkJDSWWhOS6"
        }

        b_data = {
            "to": fcm_token,
            "data": {
                "title": "Here is a good news for you!",
                "message": f"We found {count} match results of your lost dog!",
                "actual_image": ac_img,
                "match_img": mat_img
            }
        }

        print(b_data)
        fb_url = 'https://fcm.googleapis.com/fcm/send'
        response = requests.post(fb_url,
                                 data=json.dumps(b_data), headers=_headers)

        if response.status_code == 200:
            message = "Notification sent to the user!"
        else:
            message = "Some error occurred while sending notification"
        return message



@celery.task(name="main.run_models_in_background")
def run_models_in_background(img_pth, img_name, user_id, url, is_lost, lat, lng, email):
    app = create_app()
    with app.app_context():
        extractor_outputs = dog_extractor(img_pth)
        breeds = predict_breed(img_pth)
        breed_tup = tuple(breeds)
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

        query = "select * from pets where is_lost = " + str(find_status) + " and breed in " + str(breed_tup)
        fetch_pets = db_session.execute(query)
        # all_pets_filtered = pets_up_schema.dump(fetch_pets)
        # print(all_pets_filtered)
        # fetch_pets = db_session.query(Pets).filter_by(is_lost=find_status)
        db_session.close()
        all_pets = pets_up_schema.dump(fetch_pets)

        similar_dogs = []
        if len(all_pets) > 0:
            for each_val in all_pets:
                comparison = sigmoid(torch.FloatTensor(comparator_outputs),
                                     torch.FloatTensor(each_val['dog_identification']))
                comparison = comparison.tolist()
                comparison = comparison[0]
                each_val['c_score'] = comparison
                del each_val['dog_identification']
                similar_dogs.append(each_val)

            similar_dogs = pd.DataFrame.from_records(similar_dogs)
            similar_dogs = similar_dogs.sort_values(by=['c_score'], ascending=False)
            similar_dogs = similar_dogs.head(5)
            similar_dogs = similar_dogs.to_dict('records')
            os.remove(img_name)

        # DB entry after first model response
        pets = Pets(
            user_id=user_id,
            image_url=url,
            is_lost=int(is_lost),
            dog_extractor=extractor_outputs,
            dog_identification=comparator_outputs,
            final_output=similar_dogs,
            breed=breeds[0],
            lat=float(lat),
            lng=float(lng),
            contact_email=email
        )
        db_session.add(pets)
        db_session.commit()
        db_session.close()

        similar_dog_url = url

        if len(similar_dogs) > 0:
            similar_dog_url = similar_dogs[-1]['image_url']

        data = {
            "status": True,
            "stacked_comparision": similar_dogs,
            "image_url": url
        }
        noti_message = sendNotificationToLostDogUser(user_id, db_session, len(similar_dogs), url, similar_dog_url)
        user_email = db_session.query(User.email).filter_by(id=user_id).first()[0]
        mail_status = send_email_to_user(similar_dogs, user_email, len(similar_dogs), url)
        return {"data": data, "email_status":  mail_status, "notification_response": noti_message}

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
        kwargs['email'] = _results[1].email

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
    email = kwargs['email']

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
    lat = request.form.get('lat', '49.191855')
    lng = request.form.get('lng', '-122.867152')

    run_models_in_background.delay(img_pth, img_name, user_id, url, is_lost, lat, lng, email)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

#  pip freeze > requirements.txt
#  celery -A app.celery worker --loglevel=INFO