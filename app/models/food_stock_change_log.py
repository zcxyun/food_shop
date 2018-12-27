from sqlalchemy import Column, Integer, String

from app.models.base import Base


class FoodStockChangeLog(Base):
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, nullable=False, comment='食物ID')
    unit = Column(Integer, nullable=False, comment='变更多少')
    total_stock = Column(Integer, nullable=False, comment='变更之后总量')
    note = Column(String(100), nullable=False, comment='备注')
