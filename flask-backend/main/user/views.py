import json
import random
import string
from flask import request, jsonify
from sqlalchemy import delete
from main.models import db, User, users_schema, UserSession
from main.user.middleware import handle_all_exceptions
from . import user


@user.route('/register', methods=['POST'])
@handle_all_exceptions
def register():
    register_data = request.data
    register_data = json.loads(register_data)

    print(register_data)

    _res = db.session.query(User.id).filter_by(email=register_data['email']).first()

    if _res is not None:
        _error = {
            "status": False,
            "message": "Seems you already have an account. Please sign-in!"
        }
        return jsonify(_error)

    _user = User(
        name=register_data['name'],
        email=register_data['email'],
        phone=register_data['phone'],
        password=register_data['password'])
    db.session.add(_user)
    db.session.commit()

    _data = {
        "status": True,
        "message": "User registered successfully!",
    }
    return jsonify(_data)

@user.route('/login', methods=['POST'])
@handle_all_exceptions
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

@user.route('/logout', methods=['POST'])
@handle_all_exceptions
def dispose_refresh_token():
    logout_data = json.loads(request.data)

    rt = logout_data['refresh_token']
    sql1 = delete(UserSession).where(UserSession.refresh_token == rt)
    db.session.execute(sql1)
    db.session.commit()

    _data = {
        "status": True,
        "message": "Logged out successfully!",
    }
    return jsonify(_data)

@user.route('/getUsers')
def getusers():
    users = User.query.all()
    return jsonify(users_schema.dump(users))
