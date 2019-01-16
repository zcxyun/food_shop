from flask import render_template
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_codes import ServerException
from app.models import AppErrorLog

app = create_app()


@app.errorhandler(Exception)
def framework_errors(e):
    if isinstance(e, APIException):
        # AppErrorLog.add_error_log(e.msg)
        if type(e.msg) == str and e.msg.startswith('<!DOCTYPE html>'):
            return e.msg
        return e
    if isinstance(e, HTTPException):
        # AppErrorLog.add_error_log(e.description)
        code = e.code
        error_code = 1007
        msg = e.description
        return APIException(code, error_code, msg)
    else:
        # AppErrorLog.add_error_log(str(e))
        if app.config['DEBUG']:
            raise e
        else:
            return render_template('500.html')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
