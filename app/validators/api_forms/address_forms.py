from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

from app.validators.base import BaseForm


class NewAddressForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='收货人姓名不能为空')])
    mobile = StringField(validators=[DataRequired(message='收货人手机号不能为空'),
                                     Regexp(r'^1[0-9]{10}$', message='手机号码必须是11位数字')])
    province = StringField(validators=[DataRequired(message='省份不能为空')])
    city = StringField(validators=[DataRequired(message='市不能为空')])
    county = StringField(validators=[DataRequired(message='县不能为空')])
    detail = StringField(validators=[DataRequired(message='详细地址不能为空')])
