import json

from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import DataRequired, NumberRange

from app.validators.base import BaseForm


class IDMustBePositive(BaseForm):
    id = IntegerField(validators=[DataRequired(message='ID不能为空'),
                                  NumberRange(min=0, message='ID必须为正整数')])
    # id = StringField(validators=[DataRequired(message='ID不能为空')])

    # def validate_id(self, field):
    #     if not field.data.isdigit() or int(field.data) < 1:
    #         raise ValidationError('id必须为正整数')
    #     self.id.data = int(field.data)


class GoodsForm(BaseForm):
    goods = StringField(validators=[DataRequired(message='商品参数不能为空')])

    def validate_goods(self, field):
        try:
            data = json.loads(field.data)
        except Exception:
            raise ValidationError('商品参数不是有效的json格式')
        self.goods.data = data
