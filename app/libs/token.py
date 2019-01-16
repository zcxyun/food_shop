from collections import namedtuple
from flask import current_app, request, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.libs.error_codes import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

Member = namedtuple('Member', 'id scope')
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    member = verify_token(token)
    if not member:
        return False
    else:
        g.member = member
        return True


def gene_token(id, scope=None, expriation=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expriation)
    return s.dumps({
        'id': id,
        'scope': scope
    }).decode('ascii')


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('ascii'))
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    id = data['id']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return Member(id, scope)
