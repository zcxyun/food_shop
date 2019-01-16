from sqlalchemy import Column, Integer, String, ForeignKey

from . import db
from . import Base


class FoodStockChangeLog(Base):
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False, comment='食物ID')
    stock_ago = Column(Integer, nullable=False, comment='变更之前总量')
    stock = Column(Integer, nullable=False, comment='变更之后总量')
    unit = Column(Integer, nullable=False, comment='变更多少')
    note = Column(String(100), nullable=False, comment='备注')

    @staticmethod
    def set_stock_change_log(food_id, stock_ago, stock, note):
        if food_id <= 0:
            return False
        quantity = stock - stock_ago
        if quantity == 0:
            return False
        with db.auto_commit():
            log = FoodStockChangeLog()
            log.food_id = food_id
            log.stock_ago = stock_ago
            log.stock = stock
            log.unit = quantity
            log.note = note
            db.session.add(log)
        return True
