import json

from flask import request
from flask_login import current_user
from sqlalchemy import Column, Integer, String, Text

from . import db
from . import Base


class AppAccessLog(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, comment='用户ID')
    refer_url = Column(String(255), comment='当前访问的refer')
    target_url = Column(String(255), comment='访问的url')
    query_params = Column(Text, comment='get和post参数')
    ua = Column(String(255), comment='访问的user-agent')
    ip = Column(String(32), comment='访问ip')
    note = Column(String(1000), comment='json格式备注字段')

    @staticmethod
    def add_access_log():
        with db.auto_commit():
            info = AppAccessLog()
            info.target_url = request.url
            info.refer_url = request.referrer
            info.ip = request.remote_addr
            info.query_params = json.dumps(request.values.to_dict())
            if current_user.is_authenticated:
                info.uid = current_user.id
            info.ua = request.headers.get("User-Agent")
            db.session.add(info)
        return True
