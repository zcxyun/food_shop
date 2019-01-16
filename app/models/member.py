from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship

from . import Base


class Member(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False, unique=True, comment='会员昵称')
    mobile = Column(String(11), default='', comment='会员手机号码')
    sex = Column(SmallInteger, default=0, comment='性别: 0, 未选择; 1, 男; 2, 女')
    avatar = Column(String(200), comment='头像')
    reg_ip = Column(String(100), comment='注册IP')
    auth = Column(SmallInteger, nullable=False, default=1, comment='用户权限: 1, UserScope; 2, AdminScope')

    addresses = relationship('MemberAddress', backref='member', lazy='dynamic')
    carts = relationship('MemberCart', backref='member', lazy='dynamic')
    clients = relationship('MemberClient', backref='member', lazy='dynamic')
    comments = relationship('MemberComment', backref='member', lazy='dynamic')
    wx_share_histories = relationship('WxShareHistory', backref='member', lazy='dynamic')
    stat_daily_members = relationship('StatDailyMember', backref='member', lazy='dynamic')
