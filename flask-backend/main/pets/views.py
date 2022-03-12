import os
import uuid
import boto3
import torch
from . import pets
import pandas as pd
from PIL import Image
from main.models import db, Pets, pets_s_schema, pets_up_schema
from flask import request, jsonify
from main.user.middleware import logged_in, handle_all_exceptions
from main.dog_detection_demo.extractor import dog_extractor
from main.dog_identification_demo.comparator import dog_comparator, sigmoid


@pets.route('/', methods=['POST'])
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

    client = boto3.client('s3',region_name='us-west-2',
                      aws_access_key_id=os.environ['AWS_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET'])
    client.upload_file(
        Bucket=bucket,
        Filename=img_name,
        Key=img_name
    )

    img_pth = cwd + '/' + img_name
    extractor_outputs = dog_extractor(img_pth)

    if extractor_outputs[0]['boxes'] == []:
        os.remove(img_name)
        data = {
            "status": True,
            "dog_extractor":  None,
            "dog_identification": None,
            "image_url":  None
        
        }

        return jsonify(data)


    comparator_outputs = dog_comparator(img_pth, extractor_outputs[0]['boxes'])


    find_status = 0
    if int(request.form.get('lost', 0)) == 1:
        find_status = 0
    else:
        find_status = 1

    fetch_pets = db.session.query(Pets).filter_by(is_lost=find_status)
    all_pets = pets_up_schema.dump(fetch_pets)

    stacked_comparision = []

    for each_val in all_pets:
        comparison = sigmoid(torch.FloatTensor(comparator_outputs), torch.FloatTensor(each_val['dog_identification']))
        comparison = comparison.tolist()
        comparison = comparison[0]
        each_val['c_score'] = comparison
        del each_val['dog_identification']
        stacked_comparision.append(each_val)

    similar_dogs = pd.DataFrame(stacked_comparision)

    sorted_similar_dogs = similar_dogs.sort_values(by=['c_score']).head(3)

    display = sorted_similar_dogs.to_dict('records')

    os.remove(img_name)

    url = 'https://imagescmpt.s3.us-west-2.amazonaws.com/' + img_name

    pets = Pets(
        user_id = user_id,
        image_url = url,
        is_lost = int(request.form.get('lost', 0)),
        dog_extractor = extractor_outputs,
        dog_identification = comparator_outputs

    )
    db.session.add(pets)
    db.session.commit()

    data = {
        "status": True,
        "dog_extractor":  extractor_outputs,
        "dog_identification": comparator_outputs,
        "stacked_comparision": display,
        "image_url":  url
    
    }

    return jsonify(data)
