import json
from datetime import datetime

import requests
from flask_script import Manager
from sqlalchemy import func

from app.libs.enums import QueueHandleStatus, Status
from app.libs.wechat import WeChatService
from app.models import Queue, db, MemberClient, Order, FoodSaleChangeLog
from app.service.address import AddressService
from food_shop import app

queue = Manager()


@queue.command
def send_template_messages():
    """
    发送模板消息主方法
    :return:
    """
    list = Queue.query.filter_by(
        handle_status=QueueHandleStatus.UNPROCESSED.value
    ).order_by(Queue.id.asc()).limit(10).all()

    with db.auto_commit():
        for item in list:
            if item.name == 'pay':
                result = handle_pay(item)
                if not result:
                    app.logger.info('发送模板消息失败')
                    return False
                else:
                    app.logger.info('发送模板消息成功')

            item.handle_status_enum = QueueHandleStatus.PROCESSED
            db.session.add(item)


def handle_pay(item):
    """
    处理支付成功要发送模板消息的订单
    :param item:
    :return:
    """
    data = json.loads(item)
    if 'order_id' not in data or 'member_id' not in data:
        return False

    member_client = MemberClient.query.filter_by(member_id=data['member_id']).first()
    if not member_client:
        return False

    order = Order.query.filter_by(id=data['order_id']).first()
    if not order:
        return False

    resp = send_to_wechat_for_template_messages(order, member_client)
    return resp


def send_to_wechat_for_template_messages(order, member_client):
    """
    发送给微信信息以给用户发送模板消息
    :param order:
    :param member_client:
    :return:
    """
    template_data = define_template_data(order)
    wechat = WeChatService()
    access_token = wechat.get_access_token()
    headers = {'Content-Type': 'application/json'}
    url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token
    params = {
        "touser": member_client.openid,
        "template_id": "",
        "page": "pages/my/order_list",
        "form_id": order.prepay_id,
        "data": template_data
    }
    r = requests.post(url=url, data=json.dumps(params), headers=headers)
    r.encoding = 'utf-8'
    if r.status_code != 200 or not r.text:
        return False
    app.logger.info(r.text)
    return True


def define_template_data(order):
    """
    定义模板消息内容
    :param order:
    :return:
    """
    notice = update_sale_date(order)
    keyword1_val = order.note if order.note else '无'
    keyword2_val = ', '.join(notice)
    keyword3_val = str(order.total_price)
    keyword4_val = str(order.order_number)
    keyword5_val = ''
    if order.snap_address:
        address = json.loads(order.snap_address)
        keyword5_val = AddressService().set_address_info(address)
    data = {
        "keyword1": {
            "value": keyword1_val
        },
        "keyword2": {
            "value": keyword2_val
        },
        "keyword3": {
            "value": keyword3_val
        },
        "keyword4": {
            "value": keyword4_val
        },
        "keyword5": {
            "value": keyword5_val
        }
    }
    return data


def update_sale_date(order):
    """
    更新销售数据并返回模板消息内容
    :param order:
    :return:
    """
    order_foods = order.order_foods.filter_by().all()
    notice = []
    with db.auto_commit():
        if order_foods:
            date_from = datetime.strptime(
                datetime.now().strftime('%Y-%m-01 00:00:00'), '%Y-%m-%d %H:%M:%S').timestamp()
            date_to = datetime.strptime(
                datetime.now().strftime('%Y-%m-31 23:59:59'), '%Y-%m-%d %H:%M:%S').timestamp()
            for item in order_foods:
                food = item.food
                if not food:
                    continue
                notice.append('{} {}份'.format(food.name, item.quantity))

                # 当月数量
                stat_info = db.session.query(
                    func.sum(FoodSaleChangeLog.quantity).label('total')
                ).filter(
                    FoodSaleChangeLog.food_id == food.id, FoodSaleChangeLog.status == Status.EXIST.value
                ).filter(
                    FoodSaleChangeLog.create_time >= date_from, FoodSaleChangeLog.create_time <= date_to
                ).first()
                food.month_count = stat_info.total
                food.total_count += item.quantity
                db.session.add(food)
    return notice
