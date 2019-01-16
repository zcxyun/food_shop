from sqlalchemy import Column, Integer, String

from . import Base


class Image(Base):
    id = Column(Integer, primary_key=True)
    file_key = Column(String(60), nullable=False, comment='文件名')
