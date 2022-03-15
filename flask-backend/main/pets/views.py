from . import pets
from flask import jsonify
from main.user.middleware import logged_in, handle_all_exceptions
from main.models import db, User, users_schema, UserSession, Pets, pets_s_schema
from sqlalchemy import desc

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

    user_id = kwargs['user_id']
    fetch_list = db.session.query(Pets).filter_by(user_id=user_id, is_lost=1).order_by(desc(Pets.id))
    all_pets = pets_s_schema.dump(fetch_list)
    return jsonify({"status": True, "match_list": all_pets})
