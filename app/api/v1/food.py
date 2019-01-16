from flask import url_for, jsonify, current_app, g
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.libs.token import auth
from app.libs.utils import buildImageUrl
from app.models import FoodCat, Food, MemberCart, MemberComment, Member
from app.validators.api_forms.Food_forms import FoodSearchForm
from app.validators.api_forms.IDMustBePositive import IDMustBePositive
from app.view_model.api_vm.comment_vm import CommentCollection
from app.view_model.api_vm.food_vm import FoodCollection, FoodViewModel

api = Redprint('food')


@api.route('/index')
@auth.login_required
def index():
    cat_list = FoodCat.query.filter_by().order_by(FoodCat.weight.desc()).all_or_404()
    food_list = Food.query.filter_by().order_by(
        Food.total_count.desc(), Food.id.desc()).limit(3).all_or_404()

    data_cat_list = [{'id': item.id, 'name': item.name} for item in cat_list]
    data_cat_list.insert(0, {'id': 0, 'name': '全部'})

    data_food_list = []
    for item in food_list:
        tmp = {
            'id': item.id,
            'pic_url': buildImageUrl(item.main_image)
        }
        data_food_list.append(tmp)

    resp = {
        'cat_list': data_cat_list,
        'banner_list': data_food_list
    }
    return jsonify(resp)


@api.route('/search')
@auth.login_required
def search():
    form = FoodSearchForm().validate()
    page = form.page.data
    cat_id = form.cat_id.data
    query_key = form.query_key.data

    page_size = current_app.config['MINA_APP']['page_size']
    offset = (page - 1) * page_size

    query = Food.query
    if cat_id > 0:
        query = query.filter_by(cat_id=cat_id)

    if query_key:
        rule = or_(Food.name.ilike('%{}%'.format(query_key)), Food.tags.ilike('%{}%'.format(query_key)))
        query = query.filter(rule)

    food_list = query.order_by(
        Food.total_count.desc(), Food.id.desc()).offset(offset).limit(page_size).all()

    foods = []
    if food_list:
        foods = FoodCollection().fill(food_list)

    has_more = 0 if len(food_list) < page_size else 1
    data = {
        'list': foods,
        'has_more': has_more
    }
    return jsonify(data)


@api.route('/info')
@auth.login_required
def info():
    id = IDMustBePositive().validate().id.data
    food = Food.query.filter_by(id=id).first_or_404_deleted(msg='美食已下架')
    member = g.member
    cart_count = 0
    if member:
        cart_count = MemberCart.query.filter_by(food_id=food.id, member_id=member.id).count()

    info = FoodViewModel(food).hide('min_price', 'pic_url')
    resp = {
        'info': info,
        'cart_number': cart_count
    }
    return jsonify(resp)


@api.route('/comments')
def comments():
    id = IDMustBePositive().validate().id.data
    rule = MemberComment.food_ids.ilike('%_{}_%'.format(id))
    query = MemberComment.query.filter(rule).order_by(MemberComment.id.desc())
    comment_list = query.limit(5).all()
    count = query.count()

    # member_ids = [comment.member_id for comment in comment_list]
    # members = Member.query.filter(Member.id.in_(member_ids)).all()

    if comment_list:
        commemts = CommentCollection().fill(comment_list)

    resp = {
        'list': comments,
        'count': count
    }
    return jsonify(resp)
