from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import current_app
from flask import redirect, url_for
from app import db


class MyModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class MyAdminIndexView(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        return self.render('admin_index.html')

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for('auth.login'))