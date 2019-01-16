from wtforms import IntegerField, StringField, PasswordField, ValidationError
from wtforms.validators import NumberRange, Length, Regexp, DataRequired, Email, AnyOf

from app.models.user import User
from app.validators.base import BaseForm, IndexBaseForm, OpsBaseForm


class IndexForm(IndexBaseForm):
   pass


class SetForm(BaseForm):
    id = IntegerField(validators=[NumberRange(min=0, message='无效ID值')], default=0)

    nickname = StringField(validators=[DataRequired(message='昵称不允许为空'),
                                       Length(3, 22, message='昵称必须为 3 - 22 个字符')])
    mobile = StringField(validators=[DataRequired(message='手机号不允许为空'),
                                     Regexp(r'^1[0-9]{10}$', message='手机号码必须是11位数字')])
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Email(message='电子邮件格式不符合规范')])
    login_name = StringField(validators=[DataRequired(message='用户名不允许为空')])
    # Regexp(r'^1[0-9]{10}$', message='用户名码必须是11位手机号码')])
    login_pwd = PasswordField(validators=[DataRequired(message='密码不能为空'),
                                          Regexp(r'^[A-Za-z0-9_]{6,22}$',
                                                 message='密码格式不对，必须为6到22位字母，数字或下划线')])

    def validate_nickname(self, field):
        user = User.query.filter(User.nickname == field.data, User.id != self.id.data).first()
        if user:
            raise ValidationError('昵称已存在, 请再换一个试试')

    def validate_mobile(self, field):
        user = User.query.filter(User.mobile == field.data, User.id != self.id.data).first()
        if user:
            raise ValidationError('手机号已存在, 请再换一个试试')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data, User.id != self.id.data).first()
        if user:
            raise ValidationError('电子邮箱已存在, 请再换一个试试')

    def validate_login_name(self, field):
        user = User.query.filter(User.login_name == field.data, User.id != self.id.data).first()
        if user:
            raise ValidationError('用户名已存在, 请再换一个试试')


class OpsForm(OpsBaseForm):
    pass

    # def validate_id(self, field):
    #     user = User.query.get(field.data)
    #     if not user:
    #         raise ValidationError('对不起，指定账号不存在')
