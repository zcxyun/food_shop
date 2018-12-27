from sqlalchemy import Column, Integer

from app.models.base import Base


class MemberCart(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    food_id = Column(Integer, nullable=False, comment='食物ID')
    quantity = Column(Integer, nullable=False, comment='食物数量')
