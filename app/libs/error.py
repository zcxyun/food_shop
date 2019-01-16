import json

from flask import request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    error_code = 999
    msg = 'sorry, we make a mistake!'
    # data = {}

    def __init__(self, code=None, error_code=None, msg=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        # if data:
        #     self.data = data
        super(APIException, self).__init__(msg, None)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def get_body(self, environ=None):
        dict = {
            'error_code': self.error_code,
            'msg': self.msg,
            'request': request.method + ' ' + self.get_url_no_param()
            # 'data': self.data
        }
        text = json.dumps(dict)
        return text

    @staticmethod
    def get_url_no_param():
        full_path = request.full_path
        full_path_list = full_path.split('?')
        url_no_param = full_path_list[0]
        return url_no_param
