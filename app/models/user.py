from flask import request
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.error_codes import AuthFailed, Forbidden
from app.libs.scope import is_in_scope
from . import Base


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    login_name = Column(String(20), nullable=False, unique=True, comment='登录名')
    auth = Column(SmallInteger, nullable=False, default=1, comment='用户权限: 1, UserScope; 2, AdminScope')
    nickname = Column(String(24), nullable=False, unique=True, comment='用户昵称')
    mobile = Column(String(11), nullable=False, unique=True, comment='手机号')
    email = Column(String(24), nullable=False, unique=True, comment='电子邮件')
    sex = Column(SmallInteger, nullable=False, default=0, comment='性别: 0, 未选择; 1, 男; 2, 女')
    avatar = Column(String(200), nullable=False, default='', comment='头像')
    _password = Column('password', String(100), nullable=False, comment='密码')

    show_keys = ('id', 'mobile', 'nickname', 'auth')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # @staticmethod
    # def register_by_mobile(account, secret, nickname):
    #     with db.auto_commit():
    #         user = User(mobile=account, password=secret, nickname=nickname)
    #         db.session.add(user)
    @staticmethod
    def verify(account, secret):
        user = User.query.filter_by(login_name=account).first_or_404(msg='用户名或密码不对')
        if not user.check_password(secret):
            raise AuthFailed()
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        # return {'uid': user.id, 'scope': scope}
        return user

    def check_password(self, secret):
        if not self._password:
            return False
        return check_password_hash(self._password, secret)

    @login_manager.user_loader
    def load_user(uid):
        user = User.query.get(int(uid))
        if user:
            scope = 'UserScope' if user.auth == 1 else 'AdminScope'
            allow = is_in_scope(scope, request.endpoint)
            if not allow:
                raise Forbidden()
        return user

    # @login_manager.request_loader
    # def load_user_from_request(request):
    #     token = request.headers.get('Authorization')
    #     user_info = verify_token(token)
    #     user = User.query.get_or_404(user_info.uid)
    #     return user
