from flask import request
from . import pets


@pets.route('/', methods=['POST'])
def upload_lost_pet_image():
    print(request.data)
    return "hello all"

