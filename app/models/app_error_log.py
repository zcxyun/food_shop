from sqlalchemy import Column, Integer, String, Text

from app.models.base import Base


class AppErrorLog(Base):
    id = Column(Integer, primary_key=True)
    refer_url = Column(String(255), comment='当前访问的refer')
    target_url = Column(String(255), comment='访问的url')
    query_params = Column(Text, comment='get和post参数')
    content = Column(Text, nullable=False, comment='日志内容')
