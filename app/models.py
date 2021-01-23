"""
this module is about SQLAlchemy model or DB structure
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from app import db, login
import jwt
from time import time
from hashlib import md5
from flask import current_app
import json

# this table connects Users and Roles
# admin security is based on this
roles_users = db.Table('roles_users', \
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),\
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Caption(SearchableMixin, db.Model):
    __searchable__ = ['text']
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    start = db.Column(db.Float())
    duration = db.Column(db.Float())
    video_id = db.Column(db.String(100))

    def __repr__(self):
        return {'text':self.text, 'start':self.start, 'duration':self.duration, 'video_id':self.video_id}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100),index=True, unique=True)
    password_hash = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary = roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash)

    def get_token(self, expires_in=86500):
        return jwt.encode(
            {'get_token': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['get_token']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(256))