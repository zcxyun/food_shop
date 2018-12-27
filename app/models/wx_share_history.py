from sqlalchemy import Column, Integer, String

from app.models.base import Base


class WxShareHistory(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    share_url = Column(String(200), nullable=False, comment='分享的url')
