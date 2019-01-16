from flask_login import LoginManager
from .app import Flask

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    register_blueprint(app)
    register_plugins(app)
    return app


def register_blueprint(app):
    from app.api.v1 import create_blueprint_v1
    from app.cms import create_blueprint_cms
    app.register_blueprint(create_blueprint_v1(), url_prefix='/api/v1')
    app.register_blueprint(create_blueprint_cms(), url_prefix='/cms')


def register_plugins(app):
    login_manager.init_app(app)
    login_manager.login_view = 'cms.user+login'
    login_manager.login_message = '请先登录'

    from app.models import db
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()

