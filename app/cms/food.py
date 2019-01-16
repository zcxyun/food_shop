from flask import current_app, render_template, request
from flask_login import login_required
from sqlalchemy import or_

from app.models import db
from app.libs.error_codes import Success, DeleteSuccess, NotFound
from app.libs.redprint import Redprint
from app.models import Food
from app.models import FoodCat
from app.models import FoodStockChangeLog
from app.validators.cms_forms.food_forms import IndexForm, CategoryForm, CategorySetForm, CategoryOpsForm, SetForm, \
    OpsForm

cms = Redprint('food')


@cms.route('/index')
@login_required
def index():
    form = IndexForm().validate()
    q = '%{}%'.format(form.query_kw.data)
    page, status, cat_id = int(form.page.data), int(form.status.data), int(form.cat_id.data)
    resp = {
        'query_kw': form.query_kw.data,
        'status': form.status.data,
        'cat_id': form.cat_id.data
    }
    rule = or_(Food.name.ilike(q), Food.tags.ilike(q))
    query = Food.query
    if status > -1:
        query = query.filter(Food.status == status)

    cat_list = FoodCat.query.all()
    cat_mapping = {i.id: i.name for i in cat_list}

    pagination = query.filter(rule, cat_id == cat_id).order_by(Food.id.desc()).paginate(
        page, current_app.config['PAGE_SIZE'], error_out=False)
    return render_template('food/index.html', pagination=pagination, url=request.endpoint,
                           resp=resp, status_mapping=current_app.config['STATUS_MAPPING'],
                           cat_mapping=cat_mapping, current='index')


@cms.route('/info/<int:id>')
@login_required
def info(id):
    food = None
    if id:
        food = Food.query.get_or_404(id, msg='找不到指定商品')
    stock_change_list = FoodStockChangeLog.query.filter_by(food_id=id).order_by(
        FoodStockChangeLog.create_time.desc()
    ).limit(20).all()
    return render_template('food/info.html', info=food, stock_change_list=stock_change_list, current='index')


@cms.route('/set/<int:id>', methods=['POST', 'GET'])
@login_required
def set(id):
    food = None
    if id:
        food = Food.query.get_or_404_deleted(id, msg='找不到指定商品')
    cat_list = FoodCat.query.all()
    if request.method == 'POST':
        form = SetForm().validate()
        with db.auto_commit():
            if not food:
                food = Food()
            stock_ago = food.stock or 0
            food.set_attrs(form.data)
            db.session.add(food)
        FoodStockChangeLog.set_stock_change_log(food.id, stock_ago, food.stock, '后台修改')
        return Success()
    return render_template('food/set.html', info=food, cat_list=cat_list, current='index')


@cms.route('/ops/<int:id>', methods=['POST'])
@login_required
def ops(id):
    form = OpsForm().validate()
    food = Food.query.get_or_404(id, msg='找不到指定商品')
    act = form.act.data
    with db.auto_commit():
        if act == 'remove':
            food.remove()
            msg = '删除成功'
        elif act == 'recover':
            food.recover()
            msg = '恢复成功'
        db.session.add(food)
    return DeleteSuccess(msg=msg)


@cms.route('/category')
@login_required
def category():
    form = CategoryForm().validate()
    q = '%{}%'.format(form.query_kw.data)
    page, status = int(form.page.data), int(form.status.data)
    query = FoodCat.query
    if status > -1:
        query = query.filter(FoodCat.status == status)

    pagination = query.filter(FoodCat.name.ilike(q)).order_by(
        FoodCat.weight.desc(), FoodCat.id.desc()).paginate(
        page, current_app.config['PAGE_SIZE'], error_out=False)

    resp = {'query_kw': form.query_kw.data, 'status': form.status.data}

    return render_template('food/cat.html', pagination=pagination, url=request.endpoint, current='cat',
                           resp=resp, status_mapping=current_app.config['STATUS_MAPPING'])


@cms.route('/category_set/<int:id>', methods=['POST', 'GET'])
@login_required
def category_set(id):
    food_cat = None
    if id:
        food_cat = FoodCat.query.get_or_404_deleted(id, msg='未找到指定分类')
    if request.method == 'POST':
        form = CategorySetForm().validate()
        with db.auto_commit():
            if not food_cat:
                food_cat = FoodCat()
            food_cat.name = form.name.data
            food_cat.weight = form.weight.data
            db.session.add(food_cat)
        return Success()
    return render_template('food/cat_set.html', current='cat', info=food_cat)


@cms.route('/category_ops/<int:id>', methods=['POST'])
@login_required
def category_ops(id):
    form = CategoryOpsForm().validate()
    food_cat = FoodCat.query.get_or_404(id, msg='未找到指定分类')
    act = form.act.data
    with db.auto_commit():
        if act == 'remove':
            food_cat.remove()
            msg = '删除成功'
        elif act == 'recover':
            food_cat.recover()
            msg = '恢复成功'
        db.session.add(food_cat)
    return DeleteSuccess(msg=msg)
