from app.libs.error_codes import Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.user import User

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
def admin_get_user(uid):
    pass


@api.route('', methods=['GET'])
def get_user():
    user = User()
    user.mobile = '18749592518'
    user.nickname = '小汐'
    user.login_name = '18749592518'
    user.email = 'zcxyun@126.com'
    user.password = '123456'
    with db.auto_commit():
        db.session.add(user)

    return Success()


@api.route('/update')
def update_user():
    user = User.query.filter_by(mobile='18749592518').first_or_404()
    with db.auto_commit():
        user.nickname = 'superman'
        db.session.add(user)
    return Success()
