from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base


class MemberAddress(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False, comment='会员ID')
    nickname = Column(String(20), nullable=False, comment='收货人姓名')
    mobile = Column(String(11), nullable=False, comment='收货人手机号')
    province = Column(String(20), nullable=False, comment='省')
    city = Column(String(20), nullable=False, comment='市')
    county = Column(String(20), nullable=False, comment='县')
    detail = Column(String(100), nullable=False, comment='详细地址')
