from sqlalchemy import Column, Integer, String

from . import Base


class AccessToken(Base):
    id = Column(Integer, primary_key=True)
    access_token = Column(String(600), nullable=False, comment='微信的access_tokenm, 用户调用其他接口的')
    expired_time = Column(Integer, nullable=False, comment='过期时间')
