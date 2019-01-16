import json

from flask import request
from sqlalchemy import Column, Integer, String, Text

from . import db
from . import Base


class AppErrorLog(Base):
    id = Column(Integer, primary_key=True)
    refer_url = Column(String(255), comment='当前访问的refer')
    target_url = Column(String(255), comment='访问的url')
    query_params = Column(Text, comment='get和post参数')
    content = Column(Text, nullable=False, comment='日志内容')

    @staticmethod
    def add_error_log(content):
        if 'favicon.ico' in request.url:
            return
        with db.auto_commit():
            info = AppErrorLog()
            info.refer_url = request.referrer
            info.target_url = request.url
            info.query_params = json.dumps(request.values.to_dict())
            info.content = content
            db.session.add(info)
        return True
