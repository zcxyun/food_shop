from datetime import datetime, timedelta

from flask_script import Manager

from app.libs.enums import OrderStatus
from app.models import Order
from app.service.order import OrderService
from food_shop import app

pay = Manager()


@pay.command
def pay_deadline():
    now = datetime.now()
    date_30mins_ago = (now - timedelta(seconds=1)).timestamp()
    orders = Order.query.filter_by(order_status=OrderStatus.UNPAID.value).filter(
        Order.create_time <= date_30mins_ago
    ).all()
    if not orders:
        app.logger.info('没有订单数据')
        return

    for item in orders:
        OrderService.cancel_order(item)
    app.logger.info('超过30分钟未支付订单已关闭')
