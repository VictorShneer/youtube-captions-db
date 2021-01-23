import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_admin import Admin
from config import Config
from elasticsearch import Elasticsearch


db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
bootstrap = Bootstrap()
login.login_message = "Please login to view that page."



def create_app(adminFlag=True,config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    bootstrap.init_app(app)
    
    #ADMIN PANEL
    if (adminFlag):
        from app.admin.admin_sec import MyAdminIndexView
        from app.admin.admin_sec import MyModelView
        from app.models import User
        from app.models import Role
        from app.models import Caption
        from sqlalchemy import inspect
        admin=Admin()
        admin.init_app(app,index_view = MyAdminIndexView())
        admin.add_view(MyModelView(User, db.session))
        admin.add_view(MyModelView(Role, db.session))
        admin.add_view(MyModelView(Caption, db.session))


    # blueprint for auth routes in our app
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # blueprint for main routes in our app
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # blueprint for error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/your_tickle_db.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Max metrika startup')

    if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/your_tickle_db.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Your tickle db startup')

    return app

from app import models
