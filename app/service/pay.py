from app.libs.enums import OrderStatus
from app.libs.utils import now_timestamp
from app.models import db, FoodSaleChangeLog, Queue
from app.models.wx_notify_data import WxNotifyData


class PayService:

    @staticmethod
    def pay_success(order, params=None):
        with db.auto_commit(throw=False):
            if not order or order.order_status_enum != OrderStatus.UNPAID:
                return True
            order.pay_sn = params.get('transaction_id', '')
            order.order_status_enum = OrderStatus.PAID
            order.pay_time = now_timestamp()
            db.session.add(order)

            order_foods = order.order_foods.all()
            for item in order_foods:
                food_sale_log = FoodSaleChangeLog()
                food_sale_log.food_id = item.food_id
                food_sale_log.quantity = item.quantity
                food_sale_log.total_price = item.total_price
                food_sale_log.member_id = order.member_id
                db.session.add(food_sale_log)

        Queue.add_queue('pay', {
            'member_id': order.member_id,
            'order_id': order.id
        })
        return True

    @staticmethod
    def add_pay_notify_data(order, type='pay', data=''):
        with db.auto_commit():
            wx_data = WxNotifyData()
            wx_data.order_id = order.id
            if type == 'pay':
                wx_data.pay_data = data
                wx_data.refund_data = ''
            else:
                wx_data.pay_data = ''
                wx_data.refund_data = data
            db.session.add(wx_data)


