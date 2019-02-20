from app.libs.error_codes import UnderStock, Success, CartException, DeleteSuccess
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
    member = Member.query.get_or_404_deleted(g.member.id, msg='找不到指定会员')
    food = Food.query.get_or_404_deleted(id, msg='指定商品不存在')
    cart = member.carts.filter_by(food_id=food.id).first()

    with db.auto_commit():
        if not cart:
            cart = MemberCart()
            cart.food_id = food.id
            cart.member_id = member.id
        cart_count = (cart.quantity or 0) + number
        if cart_count < 0:
            raise CartException()
        if food.stock < cart_count:
            raise UnderStock()
        cart.quantity = cart_count
        db.session.add(cart)
    resp = {
        'msg': '添加购物车成功',
        'shopCarNum': cart.quantity
    }
    return jsonify(resp)


@api.route('/delete', methods=['POST'])
@auth.login_required
def delete():
    goods = GoodsForm().validate().goods.data
    member = Member.query.get_or_404_deleted(g.member.id, msg='找不到指定会员')
    with db.auto_commit():
        ids = [good['id'] for good in goods]
        carts = member.carts.filter(MemberCart.food_id.in_(ids)).all_or_404()
        for item in carts:
            db.session.delete(item)
    return DeleteSuccess()
