from sqlalchemy import Column, Integer, String, Text

from app.models.base import Base


class AppAccessLog(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, comment='用户ID')
    refer_url = Column(String(255), comment='当前访问的refer')
    target_url = Column(String(255), comment='访问的url')
    query_params = Column(Text, comment='get和post参数')
    ua = Column(String(255), comment='访问的user-agent')
    ip = Column(String(32), comment='访问ip')
    note = Column(String(1000), comment='json格式备注字段')
