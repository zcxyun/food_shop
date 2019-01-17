from app.libs.error_codes import UnderStock, Success
from app.libs.redprint import Redprint
from app.libs.token import auth
from flask import g, jsonify

from app.models import MemberCart, Food, db, Member
from app.validators.api_forms.cart_forms import SetCartForm
from app.validators.api_forms.common_forms import GoodsForm
from app.view_model.api_vm.cart_vm import CartCollection

api = Redprint('cart')


@api.route('/index')
@auth.login_required
def index():
    member = Member.query.get_or_404_deleted(g.member.id)
    cart_list = member.carts.all()
    carts = CartCollection().fill(cart_list)
    return jsonify({'list': carts})


@api.route('/set', methods=['POST'])
@auth.login_required
def set():
    form = SetCartForm().validate()
    id, number = form.id.data, form.number.data
    member = Member.query.get_or_404_deleted(g.member.id)
    food = Food.query.get_or_404_deleted(id, msg='指定商品不存在')
    if food.stock < number:
        raise UnderStock()
    cart = member.carts.filter_by(food_id=food.id).first()
    with db.auto_commit():
        if not cart:
            cart = MemberCart()
            cart.food_id = food.id
            cart.member_id = member.id
        cart.quantity = number
        db.session.add(cart)
    return Success(msg='添加购物车成功')


@api.route('/delete', methods=['POST'])
def delete():
    goods = GoodsForm().validate().goods.data
    member = Member.query.get_or_404_deleted(g.member.id)
    with db.auto_commit():
        ids = [good['id'] for good in goods]
        member.carts.filter(MemberCart.id.in_(ids)).delete()
