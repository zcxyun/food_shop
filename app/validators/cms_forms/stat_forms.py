from datetime import datetime, timedelta

from wtforms import StringField, ValidationError

from app.libs.utils import date_to_str
from app.validators.cms_forms.common_forms import SplitPageForm


class StatForm(SplitPageForm):
    date_from = StringField(
        default=date_to_str(
            datetime.now() - timedelta(days=30), format='%Y-%m-%d'
        )
    )
    date_to = StringField(default=date_to_str(format='%Y-%m-%d'))

    def validate_date_from(self, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('时间字符串格式不对')

    def validate_date_to(self, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('时间字符串格式不对')
