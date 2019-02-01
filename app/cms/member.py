from flask import request, render_template, current_app
from flask_login import login_required
from sqlalchemy import or_

from app.libs.enums import Score
from app.libs.error_codes import Success
from app.libs.redprint import Redprint
from app.models import Member, Food
from app.models import db, MemberComment, Order
from app.validators.cms_forms.common_forms import IdIsPositive, SplitPageForm, OpsForm
from app.validators.cms_forms.member_forms import MemberSetForm, MemberCommentForm
from app.view_model.cms_vm.comment_vm import CommentCollection

cms = Redprint('member')


@cms.route('/index')
@login_required
def index():
    form = SplitPageForm().validate()
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
    id = IdIsPositive().validate().id.data
    member = Member.query.get_or_404(id, msg='找不到指定会员')
    orders = member.orders.filter_by().order_by(Order.id.desc()).all()
    comments = member.comments.filter_by().order_by(MemberComment.id.desc()).all()
    resp = {
        'info': member,
        'pay_order_list': orders,
        'comment_list': comments,
        'current': 'index'
    }
    return render_template('member/info.html', **resp)


@cms.route('/set/<int:id>', methods=['POST', 'GET'])
@login_required
def set(id):
    member = Member.query.get_or_404_deleted(id, msg='找不到指定会员')
    if request.method == 'POST':
        form = MemberSetForm().validate()
        with db.auto_commit():
            member.nickname = form.nickname.data
            db.session.add(member)
        return Success()
    return render_template('member/set.html', info=member, current='index')


@cms.route('/ops/<int:id>', methods=['POST'])
@login_required
def ops(id):
    id, act = OpsForm().validate().data.values()
    member = Member.query.get_or_404(id, msg='找不到指定会员')
    with db.auto_commit():
        if act == 'remove':
            member.remove()
            msg = '删除成功'
        elif act == 'recover':
            member.recover()
            msg = '恢复成功'
        db.session.add(member)
    return Success(msg=msg)


@cms.route('/comment')
@login_required
def comment():
    form = MemberCommentForm().validate()
    page, status = int(form.page.data), int(form.status.data)
    food_id, score = form.food.data, int(form.score.data)
    query = MemberComment.query
    resp = {
        'status': form.status.data,
        'food_id': food_id,
        'score': score
    }
    if status > -1:
        query = query.filter_by(status=status)
    if food_id != '-1':
        query = query.filter(MemberComment.food_ids.ilike('%{}%'.format(food_id)))
    if score != -1:
        query = query.filter(MemberComment.score == score)
    comments_perpage = query.order_by(
        MemberComment.id.desc()).paginate(page, current_app.config['PAGE_SIZE'], error_out=False)
    foods = Food.query.all()
    comments_perpage.items = CommentCollection.fill(comments_perpage.items)

    params = {
        'pagination': comments_perpage,
        'url': request.endpoint,
        'resp': resp,
        'status_mapping': current_app.config['STATUS_MAPPING'],
        'foods': foods,
        'score_select': current_app.config['SCORE_SELECT'],
        'current': 'comment'
    }
    return render_template('member/comment.html', **params)
