from datetime import datetime, timedelta
from random import randint

from flask_script import Manager
from sqlalchemy import func

from app.libs.enums import Status, OrderStatus
from app.libs.utils import date_to_str
from app.models import Member, StatDailyMember, db, Order, WxShareHistory, FoodSaleChangeLog, StatDailyFood, \
    StatDailySite
from food_shop import app

stat = Manager()


@stat.option('-a', '--name', dest='act', metavar='act', help='job动作', required=True)
@stat.option('-d', '--date', dest='param',
             metavar='param', nargs='*', help='业务参数', required=False)
def stat_daily(act, date):
    if act not in ('member', 'food', 'site', 'test'):
        return
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return
    date_from = date + ' 00:00:00'
    date_to = date + ' 23:59:59'

    app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

    date_from_timestamp, date_to_timestamp = get_timestamp(date)

    if act == 'member':
        stat_member(date, date_from_timestamp, date_to_timestamp)
    elif act == 'food':
        stat_food(date, date_from_timestamp, date_to_timestamp)
    elif act == 'site':
        stat_site(date, date_from_timestamp, date_to_timestamp)
    elif act == 'test':
        stat_test()

    app.logger.info('统计完成')


def stat_member(date, date_from_timestamp, date_to_timestamp):
    """
    会员日统计
    :param date:
    :param date_from_timestamp:
    :param date_to_timestamp:
    :return:
    """
    members = Member.query.all()
    if not members:
        app.logger.info('会员表没有会员')
        return
    with db.auto_commit():
        for member in members:
            stat_member = member.stat_daily_members.filter_by(date=date).first()
            if not stat_member:
                stat_member = StatDailyMember()
                stat_member.member_id = member.id
                stat_member.date = date
            # 统计会员日消费总额
            stat_member_pay = db.session.query(
                func.sum(Order.total_price).label('total_pay_money')
            ).filter(
                Order.member_id == member.id, Order.status == Status.EXIST.value,
                Order.order_status != OrderStatus.UNPAID.value,
                Order.create_time >= date_from_timestamp,
                Order.create_time <= date_to_timestamp
            ).first()
            # 统计会员日分享次数
            stat_share_count = member.wx_share_histories.filter(
                WxShareHistory.status == Status.EXIST.value,
                WxShareHistory.create_time >= date_from_timestamp,
                WxShareHistory.create_time <= date_to_timestamp
            ).count()

            stat_member.total_pay_money = stat_member_pay.total_pay_money
            stat_member.total_share_count = stat_share_count
            # 模拟数据
            stat_member.total_pay_money = randint(50, 100)
            stat_member.total_share_count = randint(1000, 1010)
            db.session.add(stat_member)
    pass


def stat_food(date, date_from_timestamp, date_to_timestamp):
    """
    商品日统计
    :param date:
    :param date_from_timestamp:
    :param date_to_timestamp:
    :return:
    """
    # 从已售卖表中按商品ID分组提取 总售卖数量 总售卖价格
    stat_foods = db.session.query(
        FoodSaleChangeLog.food_id, func.sum(FoodSaleChangeLog.total_count).label('total_count'),
        func.sum(FoodSaleChangeLog.total_price).label('total_price')
    ).filter(
        FoodSaleChangeLog.status == Status.EXIST.value,
        FoodSaleChangeLog.create_time >= date_from_timestamp,
        FoodSaleChangeLog.create_time <= date_to_timestamp,
    ).group_by(FoodSaleChangeLog.id).all()

    if not stat_foods:
        app.logger.info('找不到已销售商品的数据')
        return
    # 将提取的数据放入 StatDailyFood 商品日统计表中
    with db.auto_commit():
        for item in stat_foods:
            stat_food_info = StatDailyFood.query.filter_by(food_id=item.food_id, date=date).first()
            if not stat_food_info:
                stat_food_info = StatDailyFood()
                stat_food_info.date = date
                stat_food_info.food_id = item.food_id

            stat_food_info.total_price = item.total_price
            stat_food_info.total_count = item.total_count
            # 模拟数据
            stat_food_info.total_price = randint(50, 100)
            stat_food_info.total_count = randint(1000, 1010)
            db.session.add(stat_food_info)


def stat_site(date, date_from_timestamp, date_to_timestamp):
    """
    全站日统计
    :param date:
    :param date_from_timestamp:
    :param date_to_timestamp:
    :return:
    """
    # 统计全站日收入
    stat_money = db.session.query(
        func.sum(Order.total_price).label('total_money')
    ).filter(
        Order.order_status != OrderStatus.UNPAID.value, Order.status == Status.EXIST.value,
        Order.create_time >= date_from_timestamp, Order.create_time <= date_to_timestamp
    ).first()
    # 统计全站会员总数
    stat_all_member_count = Member.query.filter_by(status=Status.EXIST.value).count()
    # 统计全站日会员总数
    stat_member_count = Member.query.filter(
        Member.status == Status.EXIST.value,
        Member.create_time >= date_from_timestamp, Member.create_time <= date_to_timestamp
    ).count()
    # 统计全站日订单总数
    stat_order_count = Order.query.filter(
        Order.status == Status.EXIST.value,
        Order.create_time >= date_from_timestamp, Order.create_time <= date_to_timestamp
    ).count()
    # 统计全站日会员分享总数
    stat_share_count = WxShareHistory.query.filter(
        WxShareHistory.status == Status.EXIST.value,
        WxShareHistory.create_time >= date_from_timestamp,
        WxShareHistory.create_time <= date_to_timestamp
    ).count()
    # 将采集的数据放入 StatDailySite 全站日统计表中
    with db.auto_commit():
        stat_site = StatDailySite.query.filter_by(date=date).first()
        if not stat_site:
            stat_site = StatDailySite()
            stat_site.date = date
        stat_site.money = stat_money
        stat_site.all_member_count = stat_all_member_count
        stat_site.member_count = stat_member_count
        stat_site.order_count = stat_order_count
        stat_site.share_count = stat_share_count

        # 模拟数据
        stat_site.money = randint(1000, 1400)
        stat_site.member_count = randint(400, 1000)
        stat_site.all_member_count += stat_site.member_count
        stat_site.order_count = randint(300, 1000)
        stat_site.share_count = randint(500, 2000)
        db.session.add(stat_site)


def stat_test():
    """
    模拟模拟数据测试统计往前一个月的数据
    :return:
    """
    now = datetime.now()
    for i in range(30, 1, -1):
        date_ago = (now - timedelta(days=i)).strftime('%Y-%m-%d')
        date_from_timestamp, date_to_timestamp = get_timestamp(date_ago)
        params = (date_ago, date_from_timestamp, date_to_timestamp)
        test_food(date_ago)
        stat_member(*params)
        stat_food(*params)
        stat_site(*params)


def test_food(date):
    """
    模拟数据 将商品表中的商品根据某一天放入已销售数据表中
    :param date:
    :return:
    """
    from app.models import Food
    foods = Food.query.all()
    with db.auto_commit():
        for item in foods:
            model = FoodSaleChangeLog()
            model.food_id = item.food_id
            model.quantity = randint(1, 10)
            model.price = model.quantity * item.price
            model.member_id = 1
            model.format_create_time = '{} {}'.format(date, date_to_str('%H:%M:%S'))
            db.session.add(model)


def get_timestamp(date):
    """
    获取某一天开始和结束的时间点的时间戳
    :param date:
    :return:
    """
    date_from = date + ' 00:00:00'
    date_to = date + ' 23:59:59'
    date_from_timestamp = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S').timestamp()
    date_to_timestamp = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S').timestamp()
    return date_from_timestamp, date_to_timestamp
