from collections import namedtuple

from flask import current_app, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_codes import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

User = namedtuple('User', 'uid scope')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    user_info = verify_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def gene_token(uid, scope=None, expriation=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expriation)
    return s.dumps({
        'uid': uid,
        'scope': scope
    }).encode('ascii')


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('ascii'))
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, scope)
