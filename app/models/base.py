from contextlib import contextmanager
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger

from app.libs.error_codes import NotFound
from app.libs.utils import now_timestamp, date_to_str


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, msg=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound(msg=msg)
        return rv

    def get_or_404_deleted(self, ident, msg=None):
        rv = self.get_or_404(ident, msg=msg)
        if rv.status == 0:
            raise NotFound(msg=msg)
        return rv

    def first_or_404(self, msg=None):
        rv = self.first()
        if not rv:
            raise NotFound(msg=msg)
        return rv

    def first_or_404_deleted(self, msg=None):
        rv = self.first_or_404(msg=msg)
        if rv.status == 0:
            raise NotFound(msg=msg)
        return rv

    def all_or_404(self, msg=None):
        rv = self.all()
        if len(rv) == 0:
            raise NotFound(msg=msg)
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer, nullable=False, default=now_timestamp, comment='创建时间')
    update_time = Column(Integer, nullable=False, default=now_timestamp, onupdate=now_timestamp, comment='更新时间')
    status = Column(SmallInteger, nullable=False, default=1, comment='用户状态: 1, 存在; 0, 删除;')

    @property
    def format_create_time(self):
        return date_to_str(datetime.fromtimestamp(self.create_time))

    @property
    def format_update_time(self):
        return date_to_str(datetime.fromtimestamp(self.update_time))

    def __getitem__(self, item):
        """对象转换为字典的必要方法"""
        return getattr(self, item)

    def keys(self):
        """对象转换为字典的必要方法"""
        return self.show_keys

    def remove(self):
        self.status = 0

    def recover(self):
        self.status = 1

    def hide(self, *keys):
        """隐藏一些属性"""
        self.show_keys = list(set(self.show_keys) - set(keys))
        return self

    def show(self, *keys):
        """只显示一些属性"""
        self.show_keys = list(set(self.show_keys) & set(keys))
        return self

    # def append(self, *keys):
    #     for key in keys:
    #         if key not in self.show_keys:
    #             self.show_keys.append(key)
    #     return self

    def set_attrs(self, attrs):
        """如果attrs是字典，并且键名符合一定规则，把键名和对象属性相同的键值赋值进来"""
        exclude_attr = ['id', 'status', 'create_time', 'update_time']
        if type(attrs) == dict:
            for key, value in attrs.items():
                if key not in exclude_attr and hasattr(self, key):
                    setattr(self, key, value)
