from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base


class MemberComment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False, comment='会员ID')
    food_ids = Column(String(200), nullable=False, comment='食物IDs')
    order_id = Column(Integer, nullable=False, comment='订单ID')
    score = Column(Integer, comment='评分')
    content = Column(String(200), default='评论内容')

    @property
    def score_desc(self):
        score_map = {
            "10": "好评",
            "6": "中评",
            "0": "差评",
        }
        return score_map[str(self.score)]
