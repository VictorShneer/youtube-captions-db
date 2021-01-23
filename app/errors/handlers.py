"""
error routes
"""
from app import db
from app.errors import bp


@bp.app_errorhandler(403)
def not_found_error(error):
    return {"message":"Forbidden"}

@bp.app_errorhandler(404)
def not_found_error(error):
    return {"message":"Not Found"}


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {"message":"Server Error"}
