from app.models.base import db
from app.models.food import Food
from app.models.food_cat import FoodCat
from app.models.app_access_log import AppAccessLog
from app.models.app_error_log import AppErrorLog
from app.models.food_sale_change_log import FoodSaleChangeLog
from app.models.food_stock_change_log import FoodStockChangeLog
from app.models.image import Image
from app.models.member import Member
from app.models.member_address import MemberAddress
from app.models.member_cart import MemberCart
from app.models.member_client import MemberClient
from app.models.member_comment import MemberComment
from app.models.order import Order
from app.models.order import OrderFood
from app.models.stat_daily_food import StatDailyFood
from app.models.stat_daily_member import StatDailyMember
from app.models.stat_daily_site import StatDailySite
from app.models.user import User
from app.models.wx_share_history import WxShareHistory

from food_shop import app

with app.app_context():
    db.create_all()


def food_cat_data():
    with app.app_context():
        with db.auto_commit():
            food_cat = FoodCat()
            food_cat.name = ''


def food_data():
    with app.app_context():
        with db.auto_commit():
            food = Food.query.get(1)
            # foodcat = food.food_cat
            # food = db.session.query(Food).all()
            # for i in food:
            #     print(i.food_cat)
        return


food_data()


def user_data():
    with app.app_context():
        with db.auto_commit():
            for i in range(0, 10):
                user = User()
                user.mobile = '18749592' + str(i)
                user.nickname = '小' + str(i)
                user.login_name = 'a' + str(i)
                user.email = 'zcxyun@1{}.com'.format(str(i))
                user.password = '123456'
                db.session.add(user)


# user_data()
