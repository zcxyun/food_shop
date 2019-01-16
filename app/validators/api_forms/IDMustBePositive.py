from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class IDMustBePositive(BaseForm):
    id = StringField(validators=[DataRequired(message='ID不能为空')])

    def validate_id(self, field):
        if not field.data.isdigit() or int(field.data) < 1:
            raise ValidationError('id必须为正整数')
