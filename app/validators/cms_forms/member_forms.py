from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

from app.validators.base import BaseForm, IndexBaseForm


class IndexForm(IndexBaseForm):
    pass


class SetForm(BaseForm):
    id = IntegerField(validators=[DataRequired(message='会员ID不允许为空'), NumberRange(
        min=1, message='会员ID须大于等于1')])
    nickname = StringField(validators=[DataRequired(message='昵称不允许为空'), Length(
        2,22, message='昵称为2到22个字符')])

