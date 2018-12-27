from sqlalchemy import Column, Integer, String, SmallInteger

from app.models.base import Base


class FoodCat(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, comment='食物种类名')
    weight = Column(SmallInteger, nullable=False, default=1, comment='权重')
