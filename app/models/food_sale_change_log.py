from sqlalchemy import Column, Integer, Float

from app.models.base import Base


class FoodSaleChangeLog(Base):
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, nullable=False, comment='食物ID')
    quantity = Column(Integer, nullable=False, comment='售卖数量')
    price = Column(Float, nullable=Float, comment='售卖金额')
    member_id = Column(Integer, nullable=Float, comment='会员ID')
