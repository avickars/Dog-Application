from . import pets
from flask import jsonify
from main.user.middleware import logged_in, handle_all_exceptions

@pets.route('/getAllUserUploadRecords', methods=['POST'])
@handle_all_exceptions
@logged_in
def upload_lost_pet_image(*args, **kwargs):
    return jsonify({})
