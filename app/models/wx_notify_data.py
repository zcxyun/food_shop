from sqlalchemy import Column, Integer, ForeignKey, String, Text

from . import Base


class WxNotifyData(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False, comment='支付订单id')
    pay_data = Column(Text, nullable=False, comment='支付完微信通知信息')
    refund_data = Column(Text, nullable=False, comment='退款完微信通知信息')
