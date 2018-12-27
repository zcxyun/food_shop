from sqlalchemy import Column, Integer, String

from app.models.base import Base


class MemberComment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    food_ids = Column(String(200), nullable=False, comment='食物IDs')
    order_id = Column(Integer, nullable=False, comment='订单ID')
    score = Column(Integer, comment='评分')
    content = Column(String(200), default='评论内容')
