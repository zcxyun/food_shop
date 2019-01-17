from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import DataRequired, NumberRange

from app.validators.base import BaseForm


class FoodSearchForm(BaseForm):
    cat_id = IntegerField(validators=[NumberRange(min=0, message='商品种类ID必须为正整数')], default=0)
    query_key = StringField(default='')
    page = IntegerField(validators=[NumberRange(min=0, message='商品种类ID必须为正整数')], default=1)

    # def validate_cat_id(self, field):
    #     if not field.data.isdigit() or int(field.data) < 0:
    #         raise ValidationError('商品种类ID必须为正整数')
    #     self.cat_id.data = int(field.data)
    #
    # def validate_page(self, field):
    #     if not field.data.isdigit() or int(field.data) < 1:
    #         raise ValidationError('页码不能小于1')
    #     self.page.data = int(field.data)
