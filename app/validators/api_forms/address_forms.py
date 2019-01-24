from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

from app.validators.base import BaseForm


class NewAddressForm(BaseForm):
    userName = StringField(validators=[DataRequired(message='收货人姓名不能为空')])
    postalCode = StringField(default='')
    telNumber = StringField(validators=[DataRequired(message='收货人手机号不能为空')])
    provinceName = StringField(validators=[DataRequired(message='省份不能为空')])
    cityName = StringField(validators=[DataRequired(message='市不能为空')])
    countyName = StringField(validators=[DataRequired(message='县不能为空')])
    detailInfo = StringField(validators=[DataRequired(message='详细地址不能为空')])
    nationalCode = StringField(default='')
    errMsg = StringField(default='')
