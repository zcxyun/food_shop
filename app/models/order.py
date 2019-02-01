from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, SmallInteger, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.libs.enums import OrderStatus
from app.libs.error_codes import OrderStatusException
from app.libs.utils import date_to_str
from . import Base
from . import OrderFood


class Order(Base):
    id = Column(Integer, primary_key=True)
    order_sn = Column(String(40), nullable=False, comment='随机订单号')
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False, comment='会员ID')
    total_price = Column(DECIMAL, nullable=False, comment='订单应付金额')
    total_count = Column(Integer, nullable=False, comment='订单商品总数')
    freight = Column(DECIMAL, default=0.00, comment='运费')
    pay_price = Column(DECIMAL, nullable=False, comment='订单实付金额')
    pay_time = Column(Integer, nullable=False, comment='会员支付到账时间')
    pay_sn = Column(String(128), comment='第三方流水号')
    prepay_id = Column(String(128), comment='第三方预付ID,订单微信支付的预订单id（用于发送模板消息）')
    note = Column(Text, comment='备注信息')
    order_status = Column(SmallInteger, nullable=False, default=0,
                          comment='订单状态: 0, 待支付; 1, 待发货; 2, 待收货; 3, 待评价; -1, 已关闭;')
    snap_img = Column(String(255), nullable=False, comment='订单快照图片')
    snap_name = Column(String(80), nullable=False, comment='订单快照名称')
    # {"userName": "", "postalCode": "", "provinceName": "", "cityName": "", "countyName": "",
    # "detailInfo": "", "nationalCode": "", "telNumber": "", "errMsg": "chooseAddress:ok"}
    snap_address = Column(String(500), nullable=False, comment='订单地址快照')
    # [{"id": 3, "count": 3, "name": "", "p_total_price": "39",
    # "p_price": "13", "main_image": "20190114/e71250679a9d406cbd6ab9ca44d7e695.jpg"}...]
    snap_items = Column(Text, nullable=False, comment='订单其他信息快照（json)')

    foods = relationship('Food', secondary=OrderFood.__table__,
                         backref=backref('orders', lazy='dynamic'), lazy='dynamic')
    order_foods = relationship('OrderFood', backref='order', lazy='dynamic')

    comments = relationship('MemberComment', backref='order', lazy='dynamic')

    show_keys = (
        'id', 'order_sn', 'member_id', 'total_price', 'total_count', 'freight', 'pay_price',
        'note', 'order_status', 'snap_img', 'snap_name', 'snap_address', 'snap_items',
        'order_status_enum', 'order_status_desc', 'order_number', 'format_pay_time', 'foods_finance',
        'format_create_time'
    )

    @property
    def order_status_enum(self):
        try:
            status = OrderStatus(self.order_status)
        except Exception:
            raise OrderStatusException()
        return status

    @order_status_enum.setter
    def order_status_enum(self, status):
        if type(status) == OrderStatus:
            self.order_status = status.value
        else:
            raise OrderStatusException()

    @property
    def order_status_desc(self):
        status_map = {
            OrderStatus.UNPAID: '待支付',
            OrderStatus.PAID: '已支付，待发货',
            OrderStatus.DELIVERED: '已发货，待收货',
            OrderStatus.NOCOMMENT: '已收货，待评价',
            OrderStatus.DONE: '已评价',
            OrderStatus.CLOSE: '已关闭'
        }
        return status_map[self.order_status_enum] if self.order_status_enum in status_map else '订单状态不正确'

    @property
    def order_number(self):
        order_number = self.date_create_time.strftime('%Y%m%d%H%M%S')
        order_number += str(self.id).zfill(5)
        return order_number

    @property
    def format_pay_time(self):
        return date_to_str(datetime.fromtimestamp(self.pay_time))

    # @property
    # def foods_finance(self):
    #     return [{
    #         'name': item.food.name,
    #         'quantity': item.quantity,
    #         'total_price': item.total_price
    #     } for item in self.order_foods]
