import json
import random
import string
from flask import request, jsonify, render_template
from sqlalchemy import delete
from main.models import db, User, users_schema, UserSession, user_schema
from main.user.middleware import handle_all_exceptions
from . import user
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config


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
        email=register_data['email'],
        fcm_token=register_data['fcm_token'],
        password=register_data['password'],
    )
    db.session.add(_user)
    db.session.flush()
    db.session.commit()

    letters = string.ascii_letters
    refresh_token = ''.join(random.choice(letters) for i in range(30))

    _user_session = UserSession(
        refresh_token=refresh_token,
        user_id=_user.id,
        device_type="MOBILE"
    )
    db.session.add(_user_session)
    db.session.commit()

    _data = {
        "status": True,
        "message": "User registered successfully!",
        "refresh_token": refresh_token
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
    fcm_token = login_data['fcm_token'],

    _res = db.session.query(User.id, User.fcm_token).filter_by(email=email, password=password).first()

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

    User.query.filter_by(id=_user_id).update(
        dict(fcm_token=fcm_token))

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

@user.route('/send', methods=['POST'])
def sendNotificationToLostDogUser():
    logout_data = json.loads(request.data)
    user_id = logout_data['user_id']

    _res = db.session.query(User.id, User.fcm_token).filter_by(id=user_id).first()

    if _res is not None:
        fcm_token = _res[1]
        _headers = {
            "Content-Type": "application/json",
            'Authorization': "key=AAAAM9hqUJ4:APA91bGuUaPEC6EcsTZBBCcQD29CZ-tG9dSx0rXsklvB_DZSXr6HX4Q9EkNJYW-1BHLoLVijWE8sSE8AM9S8am0KU0tnHofU5v0a57_nmQyOR_6ybl_ZqEXGu94m5Dv6igkJDSWWhOS6"
        }

        b_data = {
            "to": fcm_token,
            "notification": {
                "title": "Check this Mobile (title)",
                "body": "Rich Notification testing (body)",
                "mutable_content": True,
                "sound": "Tri-tone"
            },
            "data": {
                "url": "<url of media image>",
                "dl": "<deeplink action on tap of notification>"
            }
        }
        fb_url = 'https://fcm.googleapis.com/fcm/send'
        response = requests.post(fb_url,
                                 data=json.dumps(b_data), headers=_headers)

        if response.status_code == 200:
            message = "Notification sent to the user!"
            # Code here will only run if the request is successful
        else:
            message = "Some error occurred while sending notification"

    return {"message": message}


@user.route('/getUsers')
def getusers():
    users = User.query.all()
    return jsonify(users_schema.dump(users))



def format_data_for_email_temp(data=[]):
    md = []
    i = 0
    for d in data:
        idx = data.index(d)
        if i % 2 == 0:
            dn = []
        if len(dn) < 3:
            dn.append(d)
        if len(dn) == 2 or idx == (len(data) - 1):
            md.append(dn)
        i += 1
    return md


@user.route('/sendEmail')
def sendEmail():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    SITE_ROOT = "/".join(SITE_ROOT.split("/")[:-1])
    json_url = os.path.join(SITE_ROOT, 'static', 'mail_test_data.json')
    data = json.load(open(json_url))
    print(data)

    API_KEY = config('SEND_GRID_API_KEY', default='')
    if API_KEY == '':
        API_KEY = os.environ['SEND_GRID_API_KEY']

    _d = format_data_for_email_temp(data)

    _message_body = {
        "title": "Here is a good news for you!",
        "message": "We found 3 match results of your lost dog.",
        "banner_img": "https://i.imgur.com/jcP2YnQ.png",
        "input_img": "https://i.imgur.com/0F2598w.png",
        "matched_results": _d
    }

    message = Mail(
        from_email='cmpt733dogapp@gmail.com',
        to_emails='anant.awasthy29@gmail.com',
        subject='Your Dog Status',
        html_content=render_template('email/emailTemp2.html', **_message_body),
        is_multiple=True
    )
    try:
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    users = User.query.all()
    return jsonify(users_schema.dump(users))



@user.route('/viewTemp')
def viewTemp():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    SITE_ROOT = "/".join(SITE_ROOT.split("/")[:-1])
    json_url = os.path.join(SITE_ROOT, 'static', 'mail_test_data.json')
    data = json.load(open(json_url))
    print(data)

    _d = format_data_for_email_temp(data)

    _message_body = {
        "title": "Here is a good news for you!",
        "message": "We found 3 match results of your lost dog.",
        "banner_img": "https://i.imgur.com/jcP2YnQ.png",
        "input_img": "https://i.imgur.com/0F2598w.png",
        "matched_results": _d
    }
    return render_template('email/emailTemp2.html', **_message_body)
