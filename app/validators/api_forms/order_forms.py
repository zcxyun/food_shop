import json

from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import DataRequired, AnyOf

from app.libs.enums import OrderStatus
from app.validators.api_forms.common_forms import GoodsForm
from app.validators.base import BaseForm


class OrderCreateForm(GoodsForm):
    type = StringField(default='')
    address = StringField(validators=[DataRequired(message='地址不能为空')])

    def validate_address(self, field):
        try:
            data = json.loads(field.data)
        except Exception:
            raise ValidationError('地址为无效的json格式')
        if not data:
            raise ValidationError('地址不能为空')
        self.address.data = data


class OrderStatusForm(BaseForm):
    status = IntegerField(validators=[AnyOf(
        [OrderStatus.UNPAID.value, OrderStatus.PAID.value, OrderStatus.DELIVERED.value,
         OrderStatus.NOCOMMENT.value, OrderStatus.DONE.value, OrderStatus.CLOSE.value],
        message='订单状态不符合规范'
    )], default=OrderStatus.UNPAID.value)

    def validate_status(self, field):
        try:
            status = OrderStatus(field.data)
        except Exception:
            raise ValidationError('订单状态不符合规范')
        self.status.data = status


class OrderSnForm(BaseForm):
    order_sn = StringField(validators=[DataRequired(message='订单号不能为空')])


class OrderOpsForm(OrderSnForm):
    act = StringField(validators=[AnyOf(['cancel', 'confirm'], message='无效操作')])
