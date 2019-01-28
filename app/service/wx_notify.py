from flask import current_app, request

from app.libs.enums import OrderStatus
from app.libs.wechat import WeChatService
from app.models import Order
from app.service.pay import PayService


class WxNotify:

    @staticmethod
    def notify_process():
        resp = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
        mina_config = current_app.config['MINA_APP']
        wechat = WeChatService(merchant_key=mina_config['paykey'])
        notify_data = wechat.xml_2_dict(request.data)
        current_app.logger.info(notify_data)
        header = {'Content-Type': 'application/xml'}
        if notify_data['return_code'] != 'SUCCESS' or notify_data['result_code'] != 'SUCCESS':
            resp['return_code'] = resp['return_msg'] = 'FAIL'
            return wechat.dict_2_xml(resp), header

        notify_sign = notify_data['sign']
        notify_data.pop('sign')
        sign = wechat.create_sign(notify_data)
        if notify_sign != sign:
            resp['return_code'] = resp['return_msg'] = 'FAIL'
            return wechat.dict_2_xml(resp), header

        order_sn = notify_data['out_trade_no']
        order = Order.query.filter_by(order_sn=order_sn).first()
        if not order:
            resp['return_code'] = resp['return_msg'] = 'FAIL'
            return wechat.dict_2_xml(resp), header

        if int(order.total_price * 100) != int(notify_data['total_fee']):
            resp['return_code'] = resp['return_msg'] = 'FAIL'
            return wechat.dict_2_xml(resp), header

        if order.order_status_enum == OrderStatus.PAID:
            return wechat.dict_2_xml(resp), header

        PayService.pay_success(order, {'transaction_id': notify_data['transaction_id']})
        PayService.add_pay_notify_data(order, type='pay', data=request.data)
        return wechat.dict_2_xml(resp), header
