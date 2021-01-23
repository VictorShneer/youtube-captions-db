"""
main routes
"""

from flask import request
from flask import abort
from flask_login import login_required
from flask_login import current_user
from app import db
from app.main import bp
from app.models import Caption
from app.main.sec_utils import token_required

@bp.route('/get_token')
@login_required
def get_token():
    token = current_user.get_token()
    return {'token':token}


@bp.route('/write_caption/<token>', methods=['POST'])
@token_required
def write_caption(token):
    print('Token OK')
    caption_json = request.get_json()
    if not caption_json:
        abort(403)
    caption_check = Caption.query.filter_by(video_id=caption_json['video_id']).first()
    if caption_check:
        return {'message':caption_json['video_id']+' already collected'}
    caption = Caption(text=caption_json['text'], start=caption_json['start'], duration=caption_json['duration'], video_id=caption_json['video_id'])
    db.session.add(caption)
    db.session.commit()
    return {'message':'הכל בסדר'}


@bp.route('/search_for_caption/')
def search_for_caption():
    q = request.args.get('q')
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    try:
        per_page = int(request.args.get('per_page'))
    except:
        per_page = 10
    
    captions, total = Caption.search(q, page = page, per_page=per_page)
    captions = [caption.__repr__() for caption in captions.all()]
    return {'captions':captions}