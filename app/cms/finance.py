import json

from flask import current_app, request, render_template, jsonify
from flask_login import login_required

from app.libs.enums import OrderStatus, Status
from app.libs.error_codes import OrderException, Success
from app.libs.redprint import Redprint
from app.models import Order, db
from app.service.address import AddressService
from app.validators.cms_forms.common_forms import IdIsPositive, SplitPageForm
from app.validators.cms_forms.finance_forms import FinanceIndexForm, FinanceOpsForm

cms = Redprint('finance')


@cms.route('/index')
@login_required
def index():
    page, query_kw, status = FinanceIndexForm().validate().data.values()
    resp = {
        'status': status
    }
    query = Order.query
    if int(status) > -2:
        query = query.filter_by(order_status=int(status))
    pagination = query.order_by(Order.id.desc()).paginate(
        int(page), current_app.config['PAGE_SIZE'], error_out=False)
    params = {
        'pagination': pagination,
        'url': request.endpoint,
        'resp': resp,
        'current': 'index',
        'pay_status_mapping': current_app.config['PAY_STATUS_MAPPING']
    }
    return render_template('finance/index.html', **params)


@cms.route('/pay_info/<int:id>')
@login_required
def pay_info(id):
    id = IdIsPositive().validate().id.data
    order = Order.query.get_or_404_deleted(id, msg='找不到指定订单')
    member = order.member
    address = {}
    if order.snap_address:
        address = json.loads(order.snap_address)
    resp = {
        'order': order,
        'member': member,
        'address': address,
        'address_detail': AddressService().set_address_info(address),
        'current': 'index'
    }
    return render_template('finance/pay_info.html', **resp)


@cms.route('/account')
@login_required
def account():
    page = int(SplitPageForm().validate().page.data)
    total_income = 0.00
    orders_pagination = Order.query.filter(
        Order.order_status != OrderStatus.UNPAID.value,
        Order.order_status != OrderStatus.CLOSE.value,
        Order.status == Status.EXIST.value
    ).order_by(
        Order.id.desc()
    ).paginate(
        page, current_app.config['PAGE_SIZE'], error_out=False
    )
    if orders_pagination:
        total_income = sum([order.total_price for order in orders_pagination.items])
    params = {
        'pagination': orders_pagination,
        'resp': {},
        'url': request.endpoint,
        'total_income': total_income,
        'current': 'account'
    }
    return render_template('finance/account.html', **params)


@cms.route('/ops/<int:id>', methods=['POST'])
@login_required
def ops(id):
    id, act = FinanceOpsForm().validate().data.values()
    order = Order.query.get_or_404_deleted(id, msg='找不到指定订单')
    if not order.order_status_enum == OrderStatus.PAID:
        raise OrderException(msg='订单不是已支付状态，不能发货')
    with db.auto_commit():
        if act == 'deliver':
            order.order_status_enum = OrderStatus.DELIVERED
            db.session.add(order)
    return Success(msg='发货成功')
