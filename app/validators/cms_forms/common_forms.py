from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

from app.validators.base import BaseForm


class IdIsPositive(BaseForm):
    id = IntegerField(validators=[DataRequired(message='会员ID不允许为空'), NumberRange(
        min=1, message='会员ID须大于等于1')])
