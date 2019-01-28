from sqlalchemy import Column, Integer, DECIMAL, String

from . import Base


class StatDailySite(Base):
    id = Column(Integer, primary_key=True)
    date = Column(String(10), nullable=False, comment='统计日期')
    money = Column(DECIMAL, nullable=False, comment='当日应收总金额')
    all_member_count = Column(Integer, nullable=False, comment='会员总数')
    member_count = Column(Integer, nullable=False, comment='当日会员总数')
    order_count = Column(Integer, nullable=False, comment='当日订单总数')
    share_count = Column(Integer, nullable=False, comment='当日分享总数')
