from flask_login import login_required, login_user

from app.libs.redprint import Redprint
from app.libs.token import auth
from app.models.user import User

api = Redprint('token')


@api.route('')
def get_token():
    user = User.query.get_or_404(1)
    login_user(user)
    return 'success'


@api.route('/info')
@login_required
def get_token_info():
    return 'get token info'
