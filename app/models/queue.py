import json

from flask import current_app
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import QueueHandleStatus
from . import db
from . import Base


class Queue(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, comment='队列名')
    data = Column(String(500), nullable=False, comment='队列数据')
    handle_status = Column(SmallInteger, default=0, comment='处理的状态: 0, 未处理(默认) 1, 已处理')

    @staticmethod
    def add_queue(queue_name, data=None):
        with db.auto_commit():
            queue = Queue()
            queue.name = queue_name
            if data:
                queue.data = json.dumps(data)
            db.session.add(queue)

    @property
    def handle_status_enum(self):
        try:
            data = QueueHandleStatus(self.handle_status)
        except Exception as e:
            current_app.logger.info(str(e))

        return data

    @handle_status_enum.setter
    def handle_status_enum(self, data):
        if type(data) == QueueHandleStatus:
            self.handle_status = data.value
        else:
            current_app.logger.info('传入的数据不是队列处理状态枚举类型')
