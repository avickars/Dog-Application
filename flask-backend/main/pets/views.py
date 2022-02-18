from flask import request
from . import pets
from flask import Flask, request, jsonify
from PIL import Image
from flask import send_file
from main.models import db, User, users_schema, UserSession, Pets, pets_schema
import boto3
import uuid
from main.user.middleware import logged_in, handle_sql_exception
import json


@pets.route('/', methods=['POST'])
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


    uui = str(uuid.uuid4())
    img_name = uui + '.jpg'
    img.save(img_name)

    client = boto3.client('s3',
                          region_name='us-west-2',
                          aws_access_key_id='AKIAVVC3J6SQUMK34M3O',
                          aws_secret_access_key='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')
    client.upload_file(
        Bucket=bucket,
        Filename=img_name,
        Key=img_name
    )

    url = 'https://imagescmpt.s3.us-west-2.amazonaws.com/' + img_name

    _pets = Pets(
        user_id = user_id,
        image_url = url,
        breed = request.form.get('breed', ''),
        weight = float(request.form.get('weight', '')),
        height = float(request.form.get('height', '')),
        pet_name = request.form.get('pet_name', ''),
    )
    db.session.add(_pets)
    db.session.commit()

    _data = {
        "status": True,
        "message": "Image uploaded successfully!",
    }
    return jsonify(_data)


    # return jsonify({'url': url})
[4:50 PM, 2/17/2022] Anant SFU CA: import json
from functools import wraps
from flask import request, jsonify
from main.models import db, User, UserSession
from sqlalchemy.exc import SQLAlchemyError


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



def handle_sql_exception(f):
    @wraps(f)
    def applicator(*args, **kwargs):
      try:
         return f(args,*kwargs)
      except SQLAlchemyError as err:
        _error = {
          "status": False,
          "error": err._message()
        }
        return jsonify(_error)
    return applicator