from sqlalchemy import Column, Integer, Float

from app.models.base import Base


class StatDailyFood(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False, comment='统计日期')
    food_id = Column(Integer, nullable=False, comment='商品ID')
    total_count = Column(Integer, nullable=False, comment='当天售卖总数量')
    total_price = Column(Float, nullable=False, comment='当天总收入')
