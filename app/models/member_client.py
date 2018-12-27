from sqlalchemy import Column, Integer, SmallInteger, String, Text

from app.models.base import Base


class MemberClient(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    client_type = Column(SmallInteger, nullable=False, comment='客户端类型: 1, 微信小程序(目前); 2, qq;')
    openid = Column(String(80), nullable=False, comment='第三方ID, 小程序openid(目前)')
    unionid = Column(String(100), comment='小程序unionid(目前)')
    extra = Column(Text, comment='额外字段')