from flask import request
from wtforms import Form

from app.libs.error_codes import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.values.to_dict()
        view_args = request.view_args
        super(BaseForm, self).__init__(data=data, **args, **view_args)

    def validate(self):
        valid = super().validate()
        if not valid:
            msg = self.errors
            raise ParameterException(msg=msg)
        return self
