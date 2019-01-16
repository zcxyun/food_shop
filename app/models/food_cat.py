from flask import current_app
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship

from . import Base


class FoodCat(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, comment='食物种类名')
    weight = Column(SmallInteger, nullable=False, default=1, comment='权重')
    foods = relationship('Food', backref='food_cat', lazy='dynamic')

    @property
    def status_desc(self):
        return current_app.config['STATUS_MAPPING'][str(self.status)]
