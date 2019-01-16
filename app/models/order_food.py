from sqlalchemy import Column, Integer, Text, String, DECIMAL, ForeignKey

from . import Base


class OrderFood(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False, comment='订单ID')
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False, comment='商品ID')
    quantity = Column(Integer, nullable=False, comment='商品购买数量')
    total_price = Column(DECIMAL, nullable=False, comment='商品购买时的总价格: 单价 * 数量')
    food_name = Column(String(30), nullable=False, comment='商品名称快照')
    food_img = Column(String(100), nullable=False, comment='商品图片快照')
    note = Column(Text, nullable=False, comment='备注')
