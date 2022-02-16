import json
from functools import wraps
from flask import request, jsonify
from main.models import db, User, UserSession
from sqlalchemy.exc import SQLAlchemyError


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        _r = json.loads(request.data)
        _t = _r['refresh_token']
        _results = db.session.query(UserSession, User).join(UserSession).filter_by(refresh_token=_t).first()
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
         return f(*args,**kwargs)
      except SQLAlchemyError as err:
        _error = {
          "status": False,
          "error": err._message()
        }
        return jsonify(_error)
    return applicator
