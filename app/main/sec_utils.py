from flask import abort
from flask_login import current_user
from app.models import User

def token_required(function):
    def wrapper(token):
        user = User.verify_reset_token(token)
        if not user:
            abort(403)
        else:
            return function(token)
    # Renaming the function name:
    wrapper.__name__ = function.__name__
    return wrapper
