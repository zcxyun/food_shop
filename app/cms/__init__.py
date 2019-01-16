from flask import Blueprint

from app.cms import user
from app.cms import index
from app.cms import chart
from app.cms import account
from app.cms import food
from app.cms import upload
from app.cms import member


def create_blueprint_cms():
    bp = Blueprint('cms', __name__)
    user.cms.register(bp)
    index.cms.register(bp)
    chart.cms.register(bp)
    account.cms.register(bp)
    food.cms.register(bp)
    upload.cms.register(bp)
    member.cms.register(bp)
    return bp
