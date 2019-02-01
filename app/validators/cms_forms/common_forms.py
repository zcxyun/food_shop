from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Length, AnyOf

from app.validators.base import BaseForm


class IdIsPositive(BaseForm):
    id = IntegerField(validators=[DataRequired(message='ID不允许为空'), NumberRange(
        min=1, message='会员ID须大于等于1')])


class SplitPageForm(BaseForm):
    page = StringField(default='1')
    query_kw = StringField(validators=[Length(0, 24, message='查询参数必须为24个字符以内')], default='')
    status = StringField(validators=[AnyOf(['-1', '0', '1'], message='无效状态值')], default='-1')

    def validate_page(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('页码不能小于1')


class OpsForm(IdIsPositive):
    act = StringField(validators=[DataRequired(message='缺少操作标识'),
                                  AnyOf(['remove', 'recover'], message='无效操作')])
