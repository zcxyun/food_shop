from flask import request, current_app, render_template
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.libs.error_codes import ParameterException, Success, DeleteSuccess
from app.libs.redprint import Redprint
from app.models.app_access_log import AppAccessLog
from app.models.user import User
from app.validators.cms_forms.account_forms import IndexForm, SetForm, OpsForm

cms = Redprint('account')


@cms.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    form = IndexForm().validate()
    q, page, status = '%{}%'.format(form.query_kw.data), int(form.page.data), int(form.status.data)
    resp = {'query_kw': form.query_kw.data, 'status': form.status.data}
    rule = or_(User.nickname.like(q), User.mobile.like(q))
    query = User.query
    if status > -1:
        query = query.filter(User.status == status)

    pagination = query.filter(rule).order_by(User.id.desc()).paginate(
        page, current_app.config['PAGE_SIZE'], error_out=False)
    return render_template('account/index.html', pagination=pagination, url=request.endpoint,
                           resp=resp, status_mapping=current_app.config['STATUS_MAPPING'])


@cms.route('/info/<int:id>')
@login_required
def info(id):
    user = User.query.get_or_404(id)
    access_list = AppAccessLog.query.filter_by(id=id).order_by(AppAccessLog.id.desc()).limit(10).all()
    return render_template('account/info.html', user=user, access_list=access_list)


@cms.route('/set/<int:id>', methods=['POST', 'GET'])
@login_required
def set(id):
    user = None
    if id:
        user = User.query.get(id)
    if request.method == 'POST':
        form = SetForm().validate()
        with db.auto_commit():
            if not user:
                user = User()
            user.nickname = form.nickname.data
            user.login_name = form.login_name.data
            user.password = form.login_pwd.data
            user.email = form.email.data
            user.mobile = form.mobile.data
            db.session.add(user)

        return Success()
    return render_template('account/set.html', user=user)


@cms.route('/ops/<int:id>', methods=['POST'])
@login_required
def ops(id):
    form = OpsForm().validate()
    act = form.act.data
    user = User.query.get_or_404(id, msg='对不起，指定账号不存在')
    msg = ''
    with db.auto_commit():
        if act == 'remove':
            user.status = 0
            msg = '删除成功'
        if act == 'recover':
            user.status = 1
            msg = '恢复成功'
        db.session.add(user)
    return DeleteSuccess(msg=msg)


