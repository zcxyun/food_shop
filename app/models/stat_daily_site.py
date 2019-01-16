from sqlalchemy import Column, Integer, DECIMAL

from . import Base


class StatDailySite(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False, comment='统计日期')
    total_money = Column(DECIMAL, nullable=False, comment='当日应收总金额')
    total_member_count = Column(Integer, nullable=False, comment='当日会员总数')
    total_new_member_count = Column(Integer, nullable=False, comment='当日新增会员总数')
    total_order_count = Column(Integer, nullable=False, comment='当日订单总数')
    total_share_count = Column(Integer, nullable=False, comment='当日分享总数')
