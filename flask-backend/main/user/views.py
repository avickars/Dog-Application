from . import user
from main.models import db, User
from flask import request
import json


@user.route('/')
def home():
    return "hello all"

@user.route('/register', methods=['POST'])
def register():
    register_data = request.data
    register_data = json.loads(register_data)

    print(register_data)

    _user = User(
        name=register_data['name'],
        email=register_data['email'],
        phone=register_data['phone'],
        password=register_data['password'])
    db.session.add(_user)
    db.session.commit()

    return { "status" : True }

