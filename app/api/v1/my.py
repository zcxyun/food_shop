from datetime import timedelta

from app.libs.enums import OrderStatus
from app.libs.error_codes import OrderException, Success
from app.libs.redprint import Redprint
from flask import g, jsonify

from app.libs.token import auth
from app.models import Member, Order, db, MemberComment
from app.validators.api_forms.my_forms import AddCommentForm
from app.validators.api_forms.order_forms import OrderStatusForm, OrderSnForm
from app.view_model.api_vm.comment_vm import MyCommentCollection
from app.view_model.api_vm.order_vm import OrderCollection, OrderViewModel

api = Redprint('my')


@api.route('/order', methods=['POST'])
@auth.login_required
def order():
    status = OrderStatusForm().validate().status.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='指定会员不存在')
    query = member.orders
    promise = {
        OrderStatus.UNPAID: query.filter_by(order_status=OrderStatus.UNPAID.value),
        OrderStatus.PAID: query.filter_by(order_status=OrderStatus.PAID.value),
        OrderStatus.DELIVERED: query.filter_by(order_status=OrderStatus.DELIVERED.value),
        OrderStatus.NOCOMMENT: query.filter_by(order_status=OrderStatus.NOCOMMENT.value),
        OrderStatus.DONE: query.filter_by(order_status=OrderStatus.DONE.value),
        OrderStatus.CLOSE: query.filter_by(order_status=OrderStatus.CLOSE.value)
    }
    order_list = promise[status].order_by(Order.id.desc()).all_or_404(msg='订单不存在')
    order_list_vm = OrderCollection().fill(order_list)
    resp = {
        'pay_order_list': order_list_vm
    }
    return jsonify(resp)


@api.route('/order/info', methods=['POST'])
@auth.login_required
def order_info():
    order_sn = OrderSnForm().validate().order_sn.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='找不到指定会员')
    order = member.orders.filter_by(order_sn=order_sn).first_or_404(msg='指定订单不存在')
    order_vm = OrderViewModel(order)
    resp = {
        'info': order_vm
    }
    return jsonify(resp)


@api.route('/comments')
@auth.login_required
def comments():
    member = Member.query.get_or_404_deleted(g.member.id, msg='找不到指定会员')
    comment_list = member.comments.all()
    comment_list_vm = MyCommentCollection().fill(comment_list)
    resp = {
        'list': comment_list_vm
    }
    return jsonify(resp)


@api.route('/add_comment', methods=['POST'])
@auth.login_required
def add_comment():
    form = AddCommentForm().validate()
    order_sn, score, content = form.order_sn.data, form.score.data, form.content.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='找不到指定会员')
    order = member.orders.filter_by(order_sn=order_sn).first_or_404(msg='指定订单不存在')
    if order.order_status_enum == OrderStatus.DONE:
        raise OrderException(msg='订单已经评价过了, 不需要再评价了')
    food_id_list = [food.id for food in order.foods]
    food_ids_str = '_'.join(food_id_list)
    with db.auto_commit():
        comment = MemberComment()
        comment.food_ids = food_ids_str
        comment.member_id = member.id
        comment.order_id = order.id
        comment.score = score
        comment.content = content
        db.session.add(comment)

        order.order_status_enum = OrderStatus.DONE
        db.session.add(order)
    return Success(msg='添加评论成功')
