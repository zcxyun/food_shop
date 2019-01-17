from sqlalchemy import Column, Integer, String, Text, SmallInteger, DECIMAL
from sqlalchemy.orm import relationship, backref
from . import Base
from . import OrderFood


class Order(Base):
    id = Column(Integer, primary_key=True)
    order_sn = Column(String(40), nullable=False, comment='随机订单号')
    member_id = Column(Integer, nullable=False, comment='会员ID')
    total_price = Column(DECIMAL, nullable=False, comment='订单应付金额')
    total_count = Column(Integer, nullable=False, comment='订单商品总数')
    freight = Column(DECIMAL, default=0.00, comment='运费')
    pay_price = Column(DECIMAL, nullable=False, comment='订单实付金额')
    pay_sn = Column(String(128), comment='第三方流水号')
    prepay_id = Column(String(128), comment='第三方预付ID,订单微信支付的预订单id（用于发送模板消息）')
    note = Column(Text, comment='备注信息')
    order_status = Column(SmallInteger, nullable=False, default=0,
                          comment='订单状态: 0, 待支付; 1, 待发货; 2, 待收货; 3, 待评价; -1, 已关闭;')
    snap_img = Column(String(255), nullable=False, comment='订单快照图片')
    snap_name = Column(String(80), nullable=False, comment='订单快照名称')
    snap_address = Column(String(500), nullable=False, comment='订单地址快照')
    snap_items = Column(Text, nullable=False, comment='订单其他信息快照（json)')

    foods = relationship('Food', secondary=OrderFood.__table__,
                         backref=backref('orders', lazy='dynamic'), lazy='dynamic')
    order_foods = relationship('OrderFood', backref='order', lazy='dynamic')

    comments = relationship('MemberComment', backref='order', lazy='dynamic')
