from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_codes import ServerException

app = create_app()


@app.errorhandler(Exception)
def framework_errors(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        error_code = 1007
        msg = e.description
        return APIException(code, error_code, msg)
    else:
        return ServerException() if not app.config['DEBUG'] else e


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
