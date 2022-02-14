import json
import random
import string
from flask import request, jsonify
from main.models import db, User, users_schema, UserSession
from main.user.middleware import logged_in
from . import user


@user.route('/', methods=['POST'])
@logged_in
def home():
    print(request.data)
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

@user.route('/login', methods=['POST'])
def login():
    login_data = request.data
    login_data = json.loads(login_data)

    email = login_data['email']
    password = login_data['password']
    device_type = login_data['device_type']

    _res = db.session.query(User.id).filter_by(email=email, password=password).first()

    if _res is None:
        _error = {
            "status": False,
            "message": "Seems you dont have an account. Please sign-up!"
        }
        return jsonify(_error)

    _user_id = _res[0]

    letters = string.ascii_letters
    refresh_token = ''.join(random.choice(letters) for i in range(30))

    _user_session = UserSession(
        refresh_token=refresh_token,
        user_id=_user_id,
        device_type=device_type
        )

    db.session.add(_user_session)
    db.session.commit()

    _data = {
        "status": True,
        "message": "Logged in successfully!",
        "refresh_token": refresh_token
    }
    return jsonify(_data)

@user.route('/getUsers')
def getusers():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

