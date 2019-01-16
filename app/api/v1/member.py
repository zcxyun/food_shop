from flask import jsonify, g, request

from app.libs.error_codes import NotFound, Success
from app.libs.redprint import Redprint
from app.libs.token import gene_token, auth, verify_token
from app.libs.utils import get_openid
from app.models import MemberClient, Member, db, WxShareHistory
from app.validators.api_forms.member_forms import LoginForm, CodeForm, UrlForm

api = Redprint('member')


@api.route('/login', methods=['POST'])
def login():
    form = LoginForm().validate()
    openid = get_openid(form.code.data)
    if openid is None:
        raise NotFound('找不到openid')
    member_client = MemberClient.query.filter_by(openid=openid, client_type=1).first()
    if not member_client:
        with db.auto_commit():
            member = Member()
            member.nickname = form.nickName.data
            member.sex = form.gender.data
            member.avatar = form.avatarUrl.data
            db.session.add(member)
        with db.auto_commit():
            member_client = MemberClient()
            member_client.member_id = member.id
            member_client.client_type = 1
            member_client.openid = openid
            db.session.add(member_client)
    else:
        member = member_client.member
    scope = 'UserScope' if member.auth == 1 and member.status == 1 else 'AdminScope'
    token = gene_token(id=member.id, scope=scope)
    return jsonify({'token': token})


@api.route('/verify', methods=['POST'])
def verify():
    form = CodeForm().validate()
    openid = get_openid(form.code.data)
    if not openid:
        raise NotFound('找不到openid')
    member_client = MemberClient.query.filter_by(openid=openid, client_type=1).first_or_404(msg='未绑定微信')
    member = Member.query.filter_by(id=member_client.member_id).first_or_404(msg='未绑定微信')
    scope = 'UserScope' if member.auth == 1 else 'AdminScope'
    token = gene_token(id=member.id, scope=scope)
    return jsonify({'token': token})


@api.route('/verify_token', methods=['POST'])
def verify_token():
    req = request.get_json()
    token = req['token'] if 'token' in req else ''
    res = verify_token(token)
    if not res:
        raise NotFound('无效token')
    return Success()


@api.route('/share', methods=['POST'])
@auth.login_required
def share():
    form = UrlForm().validate()
    member = g.member
    if not member:
        return NotFound(msg='找不到指定会员')
    with db.auto_commit():
        share = WxShareHistory()
        share.member_id = member.id
        db.session.add(share)
    return Success()


@api.route('/info')
@auth.login_required
def info():
    member = g.member
    info = {
        'nickname': member.nickname,
        'avatar_url': member.avatar
    }
    return jsonify({'info': info})
