from flask import request
from wtforms import Form, StringField, ValidationError, IntegerField
from wtforms.validators import Length, AnyOf, NumberRange, DataRequired

from app.libs.error_codes import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.values.to_dict()
        view_args = request.view_args
        super(BaseForm, self).__init__(data=data, **args, **view_args)

    def validate(self):
        valid = super().validate()
        if not valid:
            msg = self.errors
            raise ParameterException(msg=msg)
        return self


class IndexBaseForm(BaseForm):
    page = StringField(default='1')
    query_kw = StringField(validators=[Length(0, 24, message='查询参数必须为24个字符以内')], default='')
    status = StringField(validators=[AnyOf(['-1', '0', '1'], message='无效状态值')], default='-1')

    def validate_page(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('页码不能小于1')


class OpsBaseForm(BaseForm):
    id = IntegerField(validators=[DataRequired(message='缺少操作ID'),
                                  NumberRange(min=1, message='无效ID值')])
    act = StringField(validators=[DataRequired(message='缺少操作标识'),
                                  AnyOf(['remove', 'recover'], message='无效操作')])
