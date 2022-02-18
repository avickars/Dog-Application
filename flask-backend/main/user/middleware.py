import json
from functools import wraps
from flask import request, jsonify
from main.models import db, User, UserSession
from sqlalchemy.exc import SQLAlchemyError


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        _t = request.form.get('refresh_token', '')
        if _t == '':
            _r = json.loads(request.data)
            _t = _r['refresh_token']

            if 'refresh_token' not in _r:
                _error = jsonify({
                    "status": False,
                    "message": "Seems you have not signed in. Please sign-in!"
                })
                return _error
        _results = db.session.query(UserSession, User).join(UserSession).filter_by(refresh_token=_t).first()

        if len(_results) > 0:
            if _results[0].refresh_token is None:
                _error = jsonify({
                    "status": False,
                    "message": "Seems you have not signed in. Please sign-in!"
                })
                return _error

        kwargs['user_id'] = _results[0].user_id

        if _results is not None:
            return f(*args, **kwargs)
        else:
            _error = jsonify({
                "status": False,
                "message": "Seems you have not signed in. Please sign-in!"
            })
            return _error
    return decorated_func



def handle_sql_exception(f):
    @wraps(f)
    def applicator(*args, **kwargs):
      try:
         return f(args,*kwargs)
      except SQLAlchemyError as err:
        _error = {
          "status": False,
          "error": err._message()
        }
        return jsonify(_error)
    return applicator