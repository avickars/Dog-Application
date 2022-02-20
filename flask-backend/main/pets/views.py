from . import pets
import uuid
import boto3
from PIL import Image
from flask import request, jsonify
from main.models import db, Pets
from main.user.middleware import logged_in, handle_all_exceptions
from . import pets
import os


@pets.route('/', methods=['POST'])
@handle_all_exceptions
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

    client = boto3.client('s3',region_name='us-west-2',
                      aws_access_key_id=os.environ['AWS_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET'])
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
