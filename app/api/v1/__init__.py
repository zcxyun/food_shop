from flask import Blueprint
from . import member
from . import food
from . import cart
from . import order


def create_blueprint_v1():
    bp_v1 = Blueprint('api.v1', __name__)
    member.api.register(bp_v1)
    food.api.register(bp_v1)
    cart.api.register(bp_v1)
    order.api.register(bp_v1)
    return bp_v1
