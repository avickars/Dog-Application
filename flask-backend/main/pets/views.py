from . import pets
from flask import jsonify, request
from main.user.middleware import logged_in, handle_all_exceptions
from main.models import db, User, users_schema, UserSession, Pets, pets_s_schema, in_pets_schema
from sqlalchemy import desc
import json
import os

@pets.route('/getAllUserUploadRecords', methods=['POST'])
@handle_all_exceptions
@logged_in
def get_all_matches(*args, **kwargs):

    if 'user_id' not in kwargs:
        _error = jsonify({
            "status": False,
            "message": "Seems you have not signed in. Please sign-in!"
        })
        return _error

    body = json.loads(request.data)
    user_id = kwargs['user_id']
    fcm_token = body['fcm_token']
    fetch_list = db.session.query(Pets).filter_by(user_id=user_id, is_lost=1).order_by(desc(Pets.id))

    User.query.filter_by(id=user_id).update(
        dict(fcm_token=fcm_token))
    db.session.commit()

    all_pets = pets_s_schema.dump(fetch_list)
    return jsonify({"status": True, "match_list": all_pets})



@pets.route('/addFoundDogs', methods=['POST'])
@handle_all_exceptions
def add_found_dogs(*args, **kwargs):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    SITE_ROOT = "/".join(SITE_ROOT.split("/")[:-1])
    json_url = os.path.join(SITE_ROOT, 'static', 'found_dogs.json')
    data = json.load(open(json_url))
    _d = in_pets_schema.load(data)
    db.session.bulk_insert_mappings(Pets, _d)
    db.session.commit()

    return jsonify({
        "status": True,
        "message": "All records added successfully!"
    })


@pets.route('/getAllFoundPets', methods=['POST'])
@handle_all_exceptions
def get_all_found_pets(*args, **kwargs):
    # 'lat', 'lng', 'user_id', 'image_url', 'is_lost', 'final_output', 'dog_extractor', 'dog_identification'
    fetch_list = db.session.query(Pets.lat,Pets.lng, Pets.user_id, Pets.image_url, Pets.is_lost, Pets.final_output, Pets.dog_extractor, Pets.dog_identification,Pets.breed).filter_by(is_lost=0).order_by(desc(Pets.id))
    all_pets = pets_s_schema.dump(fetch_list)
    return jsonify(all_pets)

