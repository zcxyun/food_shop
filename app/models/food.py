from sqlalchemy import Column, Integer, String, DECIMAL, Float, Text

from app.models.base import Base


class Food(Base):
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, nullable=False, comment='分类ID')
    name = Column(String(20), nullable=False, comment='食物名称')
    price = Column(Float, nullable=False, comment='食物价格')
    image = Column(String(100), nullable=False, comment='食物图片')
    summary = Column(Text, nullable=False, comment='描述')
    stock = Column(Integer, nullable=False, comment='库存量')
    tags = Column(String(200), nullable=False, comment='标签关键字 以逗号连接')
    month_count = Column(Integer, comment='月销售量')
    total_count = Column(Integer, comment='总销售量')
    view_count = Column(Integer, comment='总浏览量')
    comment_count = Column(Integer, comment='总评论量')
