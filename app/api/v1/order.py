from flask import g, jsonify

from app.libs.redprint import Redprint
from app.service.order import OrderService
from app.validators.api_forms.common_forms import GoodsForm

api = Redprint('order')


@api.route('/info', methods=['POST'])
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
