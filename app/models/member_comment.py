from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger

from app.libs.enums import Score
from app.libs.error_codes import ScoreException
from . import Base


class MemberComment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False, comment='会员ID')
    food_ids = Column(String(200), nullable=False, comment='商品ID')
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False, comment='订单ID')
    score = Column(SmallInteger, comment='评分')
    content = Column(String(200), default='评论内容')

    @property
    def score_desc(self):
        score_map = {
            2: "好评",
            1: "中评",
            0: "差评",
        }
        return score_map[self.score]

    @property
    def score_enum(self):
        try:
            data = Score(self.score)
        except ValueError as e:
            raise ScoreException()
        return data

    @score_enum.setter
    def score_enum(self, score):
        if type(score) == Score:
            self.score = score.value
        else:
            raise ScoreException()
