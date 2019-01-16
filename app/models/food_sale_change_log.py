from sqlalchemy import Column, Integer, DECIMAL, ForeignKey

from . import Base


class FoodSaleChangeLog(Base):
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False, comment='食物ID')
    quantity = Column(Integer, nullable=False, comment='售卖数量')
    price = Column(DECIMAL, nullable=False, comment='售卖金额')
    member_id = Column(Integer, nullable=False, comment='会员ID')
