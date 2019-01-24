from sqlalchemy import Column, Integer, ForeignKey, String, Text

from app.models import Base


class OrderCallbackData(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False, comment='支付订单id')
    pay_data = Column(Text, nullable=False, comment='支付回调信息')
    refund_data = Column(Text, nullable=False, comment='退款回调信息')
