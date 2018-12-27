from contextlib import contextmanager
from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger

from app.libs.error_codes import NotFound
from app.libs.utils import now_timestamp


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

    def first_or_404(self, msg=None):
        rv = self.first()
        if not rv:
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
    status = Column(SmallInteger, nullable=False, default=1, comment='用户状态: 1, 存在; 2, 删除;')

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.show_keys

    def delete(self):
        self.status = 0

    def hide(self, *keys):
        for key in keys:
            self.show_keys.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.show_keys.append(key)
        return self

    def set_attrs(self, attrs):
        exclude_attr = ['id', 'status', 'create_time', 'update_time']
        for key, value in attrs.items():
            if key not in exclude_attr and hasattr(self, key):
                setattr(self, key, value)
