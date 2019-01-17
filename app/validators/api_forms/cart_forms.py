import json

from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import DataRequired, NumberRange

from app.validators.api_forms.common_forms import IDMustBePositive
from app.validators.base import BaseForm


class SetCartForm(IDMustBePositive):
    number = IntegerField(validators=[DataRequired(message='商品数量不能为空'),
                                      NumberRange(min=0, message='商品数量必须为正整数')])
    # number = StringField(validators=[DataRequired(message='商品数量不能为空')])
    #
    # def validate_number(self, field):
    #     if not field.data.isdigit() or int(field.data) < 1:
    #         raise ValidationError('商品数量必须为正整数')
    #     self.number.data = int(field.data)


