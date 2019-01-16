from flask import request, render_template, current_app
from flask_login import login_required
from sqlalchemy import or_

from app.models import db
from app.libs.error_codes import Success
from app.libs.redprint import Redprint
from app.models import Member
from app.validators.cms_forms.member_forms import SetForm, IndexForm

cms = Redprint('member')


@cms.route('/index')
@login_required
def index():
    form = IndexForm().validate()
    q, page, status = '%{}%'.format(form.query_kw.data), int(form.page.data), int(form.status.data)
    resp = {'query_kw': form.query_kw.data, 'status': form.status.data}
    rule = or_(Member.nickname.ilike(q), Member.mobile.ilike(q))
    query = Member.query
    if status > -1:
        query = query.filter(Member.status == status)
    pagination = query.filter(rule).order_by(Member.id.desc()).paginate(
        page, current_app.config['PAGE_SIZE'], error_out=False)
    return render_template('member/index.html', pagination=pagination, url=request.endpoint,
                           resp=resp, status_mapping=current_app.config['STATUS_MAPPING'])


@cms.route('/info/<int:id>')
@login_required
def info(id):
    pass


@cms.route('/set/<int:id>', methods=['POST', 'GET'])
@login_required
def set(id):
    member = Member.query.get_or_404_deleted(id, msg='找不到指定会员')
    if request.method == 'POST':
        form = SetForm().validate()
        with db.auto_commit():
            member.nickname = form.nickname.data
            db.session.add(member)
        return Success()
    return render_template('member/set.html', info=member, current='index')


@cms.route('/ops/<int:id>', methods=['POST'])
@login_required
def ops(id):
    pass


@cms.route('/comment')
@login_required
def comment():
    pass
