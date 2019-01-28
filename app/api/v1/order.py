from flask import g, jsonify, current_app

from app.libs.enums import ClientType
from app.libs.error_codes import OrderException
from app.libs.redprint import Redprint
from app.libs.token import auth
from app.models import Member, db
from app.service.order import OrderService
from app.libs.wechat import WeChatService
from app.service.wx_notify import WxNotify
from app.validators.api_forms.common_forms import GoodsForm
from app.validators.api_forms.order_forms import OrderCreateForm, OrderOpsForm, OrderSnForm

api = Redprint('order')


@api.route('/info', methods=['POST'])
@auth.login_required
def info():
    goods = GoodsForm().validate().goods.data
    foods_resp, pay_price, freight = OrderService(goods).get_order()
    resp = {
        'food_list': foods_resp,
        'pay_price': str(pay_price),
        'yun_price': str(freight),
        'total_price': str(pay_price + freight)
    }
    return jsonify(resp)


@api.route('/create', methods=['POST'])
@auth.login_required
def create():
    form = OrderCreateForm().validate()
    goods, address, type = form.goods.data, form.address.data, form.type.data
    resp = OrderService(goods, address, type, g.member.id).create_order()
    if resp and type == 'cart':
        member = Member.query.get_or_404_deleted(g.member.id)
        with db.auto_commit():
            member.carts.delete()
    return jsonify(resp)


@api.route('/pay', methods=['POST'])
@auth.login_required
def pay():
    order_sn = OrderSnForm().validate().order_sn.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='指定会员不存在')
    order = member.orders.filter_by(
        order_sn=order_sn).first_or_404(msg='订单号有误, 指定订单不存在')

    mina_config = current_app.config['MINA_APP']
    notify_url = current_app.config['APP']['domain'] + mina_config['callback_url']

    openid = member.clients.filter_by(
        client_type=ClientType.WECHAT.value).first_or_404(msg='该微信用户不存在')
    wechat = WeChatService(merchant_key=mina_config['paykey'])

    pay_data = {
        'appid': mina_config['appid'],
        'mch_id': mina_config['mch_id'],
        'nonce_str': wechat.get_nonce_str(),
        'body': '订餐',
        'out_trade_no': order.order_sn,
        'total_fee': int(order.total_price * 100),
        'notify_url': notify_url,
        'trade_type': 'JSAPI',
        'openid': openid
    }
    pay_info = wechat.get_pay_info(pay_data)
    if pay_info:
        # 保存prepay_id为了后面发模板消息
        with db.auto_commit():
            order.prepay_id = pay_info['prepay_id']
            db.session.add(order)
    resp = {
        'pay_info': pay_info
    }
    return jsonify(resp)


@api.route('/callback', methods=['POST'])
def callback():
    return WxNotify.notify_process()


@api.route('/ops', methods=['POST'])
@auth.login_required
def ops():
    form = OrderOpsForm().validate()
    order_sn, act = form.order_sn.data, form.act.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='指定会员不存在')
    order = member.orders.filter_by(order_sn=order_sn).first_or_404(msg='订单号有误, 指定订单不存在')

    if act == 'cancel':
        return OrderService().cancel_order(order)

    if act == 'confirm':
        return OrderService().confirm_order(order)

    return OrderException(msg='无效操作')
