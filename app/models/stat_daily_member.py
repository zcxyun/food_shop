from sqlalchemy import Column, Integer, Float

from app.models.base import Base


class StatDailyMember(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False, comment='统计日期')
    member_id = Column(Integer, nullable=False, comment='会员ID')
    total_share_count = Column(Integer, nullable=False, comment='当日总分享次数')
    total_pay_money = Column(Float, nullable=False, comment='当日付款总金额')
    