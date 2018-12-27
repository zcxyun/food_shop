from sqlalchemy import Column, Integer, String, SmallInteger

from app.models.base import Base


class Member(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False, unique=True, comment='会员昵称')
    mobile = Column(String(11), nullable=False, unique=True, comment='会员手机号码')
    sex = Column(SmallInteger, default=0, comment='性别: 0, 未选择; 1, 男; 2, 女')
    avatar = Column(String(200), comment='头像')
    reg_ip = Column(String(100), comment='注册IP')

