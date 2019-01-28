from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.validators.base import IndexBaseForm
from app.validators.cms_forms.common_forms import IdIsPositive


class IndexForm(IndexBaseForm):
    pass


class SetForm(IdIsPositive):
    nickname = StringField(validators=[DataRequired(message='昵称不允许为空'), Length(
        2,22, message='昵称为2到22个字符')])

