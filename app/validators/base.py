from flask import request
from wtforms import Form

from app.libs.error_codes import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.values.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate(self):
        valid = super().validate()
        if not valid:
            msg = list(self.errors.values())[0][0]
            raise ParameterException(msg=msg)
        return self
