from sqlalchemy import Column, Integer, String, DECIMAL, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Food(Base):
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('food_cat.id'), nullable=False, comment='分类ID')
    name = Column(String(20), nullable=False, comment='食物名称')
    price = Column(DECIMAL, nullable=False, comment='食物价格', default=0.00)
    main_image = Column(String(100), nullable=False, comment='食物图片')
    summary = Column(Text, nullable=False, comment='描述')
    stock = Column(Integer, nullable=False, comment='库存量', default=0)
    tags = Column(String(200), nullable=False, comment='标签关键字 以逗号连接')
    month_count = Column(Integer, comment='月销售量', default=0)
    total_count = Column(Integer, comment='总销售量', default=0)
    view_count = Column(Integer, comment='总浏览量', default=0)
    comment_count = Column(Integer, comment='总评论量', default=0)

    sale_change_logs = relationship('FoodSaleChangeLog', backref='food', lazy='dynamic')
    stock_change_logs = relationship('FoodStockChangeLog', backref='food', lazy='dynamic')
    stat_daily_foods = relationship('StatDailyFood', backref='food', lazy='dynamic')
    order_foods = relationship('OrderFood', backref='food', lazy='dynamic')
