from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class AddCommentForm(BaseForm):
    order_sn = StringField(validators=[DataRequired(message='订单号不能为空')])
    score = IntegerField(default=10)
    content = StringField(validators=[DataRequired(message='您还没有评价, 请填写评价内容')])
