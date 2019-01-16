from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class FoodSearchForm(BaseForm):
    cat_id = StringField(validators=[DataRequired(message='商品种类不能为空')])
    query_key = StringField(default='')
    page = StringField(validators=[DataRequired(message='页数不能为空')])

    def validate_cat_id(self, field):
        if not field.data.isdigit() or int(field.data) < 0:
            raise ValidationError('商品种类ID必须为正整数')
        self.cat_id.data = int(field.data)

    def validate_page(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('页码不能小于1')
        self.page.data = int(field.data)
