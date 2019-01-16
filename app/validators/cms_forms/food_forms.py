from decimal import Decimal
from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import NumberRange, DataRequired, Length, AnyOf, Regexp

from app.validators.base import IndexBaseForm, BaseForm, OpsBaseForm


class IndexForm(IndexBaseForm):
    cat_id = StringField(default='0')

    def validate_cat_id(self, field):
        if not field.data.isdigit() or int(field.data) < 0:
            raise ValidationError('商品种类ID不能小于0')


class SetForm(BaseForm):
    id = IntegerField(validators=[NumberRange(0, message='商品ID不能小于0')], default=0)
    cat_id = StringField(validators=[DataRequired(message='请指定商品种类')])
    name = StringField(validators=[DataRequired(message='请指定商品名'), Length(
        2, 20, message='商品名必须为2到20个字符')])
    price = StringField(validators=[DataRequired(message='请指定商品价格'), Regexp(
        r'^\d+\.?\d{0,2}$', message='商品价格必须为正数，可以保留1到2个小数位')])
    main_image = StringField(validators=[DataRequired(message='请指定商品图片')])
    summary = StringField(validators=[DataRequired(message='请写一些商品信息')])
    stock = StringField(validators=[DataRequired(message='请填写商品库存')])
    tags = StringField(validators=[DataRequired(message='至少填写一个商品标签, 并按回车键确认')])

    def validate_cat_id(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('请指定商品种类')
        self.cat_id.data = int(field.data)

    def validate_price(self, field):
        self.price.data = Decimal(field.data).quantize(Decimal('0.00'))

    def validate_stock(self, field):
        if not field.data.isdigit() or int(field.data) < 0:
            raise ValidationError('商品库存不能小于0且是正整数')
        self.stock.data = int(field.data)


class OpsForm(OpsBaseForm):
    pass


class CategoryForm(IndexBaseForm):
    pass


class CategorySetForm(BaseForm):
    id = IntegerField(validators=[NumberRange(min=0, message='无效ID值')], default=0)
    name = StringField(validators=[DataRequired(message='请输入分类名'), Length(2, 10, message='分类名称是2到10个字符')])
    weight = StringField(default='1')

    def validate_weight(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('权重值必须大于等于1')


class CategoryOpsForm(OpsBaseForm):
    pass
