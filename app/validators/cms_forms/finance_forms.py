from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf

from app.validators.cms_forms.common_forms import SplitPageForm, OpsForm


class FinanceIndexForm(SplitPageForm):
    status = StringField(
        validators=[
            AnyOf(['-2', '-1', '0', '1'], message='订单状态值不正确')
        ],
        default='-2'
    )


class FinanceOpsForm(OpsForm):
    act = StringField(
        validators=[
            DataRequired(message='缺少操作标识'),
            AnyOf(['deliver'], message='无效操作')
        ]
    )
