from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length, AnyOf

from app.models import Food
from app.validators.cms_forms.common_forms import IdIsPositive, SplitPageForm


class MemberSetForm(IdIsPositive):
    nickname = StringField(validators=[DataRequired(message='昵称不允许为空'), Length(
        2, 22, message='昵称为2到22个字符')])


class MemberCommentForm(SplitPageForm):
    food = StringField(default='-1')
    score = StringField(validators=[AnyOf(['-1', '0', '1', '2'],
                                          message='所选评分不符合规范')], default='-1')

    def validate_food(self, field):
        if field.data == '-1' or not field.data.isdigit():
            return
        info = Food.query.filter(Food.id == int(field.data)).first()
        if not info:
            raise ValidationError('找不到指定产品')
        self.food.data = info.id
