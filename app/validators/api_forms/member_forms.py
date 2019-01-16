from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class CodeForm(BaseForm):
    code = StringField(validators=[DataRequired(message='微信code码不能为空')])


class LoginForm(CodeForm):
    nickName = StringField(default='')
    gender = StringField(default='')
    avatarUrl = StringField(default='')

    def validate_gender(self, field):
        if field.data.isdigit():
            self.gender.data = int(field.data)


class UrlForm(BaseForm):
    url = StringField(validators=[DataRequired(message='url不能为空')])
