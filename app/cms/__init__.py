from flask import Blueprint

from app.cms import user
from app.cms import index
from app.cms import chart
from app.cms import account


def create_blueprint_cms():
    bp = Blueprint('cms', __name__)
    user.cms.register(bp)
    index.cms.register(bp)
    chart.cms.register(bp)
    account.cms.register(bp)
    return bp
