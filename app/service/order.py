import hashlib
import json
import random
import time
from decimal import Decimal
from uuid import uuid1

from app.libs.enums import OrderStatus
from app.libs.error_codes import OrderException, Success
from app.libs.utils import buildImageUrl
from app.models import Food, db, Order, FoodStockChangeLog, OrderFood
from decimal import Decimal


class OrderService:

    def __init__(self, goods=None, address=None, type=None, member_id=None):
        """
        :param goods: like [{'id': 0, 'number': 0},...]
        :param address: {}  商品地址来自客户端, 经过校验层反序列化后传进来
        :param type: ''  指定预订单来自哪里(1: 来自立即购买, 2: 购物车)
        :param member_id:
        """
        if goods:
            self.goods = goods
            self.products_dic = {good['id']: good['number'] for good in goods}
            food_ids = self.products_dic.keys()
            self.products = db.session.query(Food).filter(
                Food.id.in_(food_ids)).with_for_update().all()
        if address:
            self.address = address
        if type:
            self.type = type
        if member_id:
            self.member_id = member_id

    def get_order(self):
        """
        从购物车得到的信息构建预订单
        :return: 商品信息列表， 总支付金额， 运费
        """
        pay_price = freight = Decimal(0.00)
        data_food_list = []
        for item in self.products:
            tmp_data = self._deal_data(item)
            data_food_list.append(tmp_data)
            pay_price += item.price * self.products_dic[item.id]

        return data_food_list, pay_price, freight

    def _deal_data(self, data):
        """
        根据单个商品信息提取指定信息
        :param data:
        :return: 指定信息
        """
        return {
            'id': data.id,
            'name': data.name,
            'total_price': str(data.price),
            'pic_url': buildImageUrl(data.main_image),
            'number': self.products_dic[data.id]
        }

    def create_order(self):
        """
        创建订单主方法
        :return:
        """
        order_status = self.get_order_status()
        # if not status['pass']:
        #     status['order_id'] = -1
        #     return status
        order_data = self.create_order_by_tran(order_status)
        return order_data

    def get_order_status(self):
        """
        获得订单表相关数据
        :return:
        """
        status = {
            # 'pass': True,
            'order_price': 0,
            'order_count': 0,
            'pStatusArray': [],
            'snap_address': json.dumps(self.address),
            'snap_name': self.products[0].name if len(self.products) == 1 else self.products[0].name + '等...',
            'snap_img': self.products[0].main_image
        }
        for item in self.goods:
            pStatus = self.get_product_status(item['id'], item['number'], self.products)
            # if not pStatus['have_stock']:
            #     status['pass'] = False
            status['order_price'] += Decimal(pStatus['p_total_price'])
            status['order_count'] += pStatus['count']
            status['pStatusArray'].append(pStatus)
        return status

    def get_product_status(self, pid, number, products):
        """
        获得订单表中单个商品的快照数据，插入订单表时需要序列化
        判断 1, pid的合法性 2, 库存量是否足, 若足就减库存，并记录在相关日志表中
        :param pid:
        :param number:
        :param products:
        :return: 单个商品快照信息
        """
        pIndex = -1
        pStatus = {
            'id': None,
            # 'have_stock': True,
            'count': 0,
            'name': '',
            'p_total_price': 0,
            'p_price': 0,
            'main_image': ''
        }
        # 客户端传递的productid有可能根本不存在
        for i, product in enumerate(products):
            if pid == product.id:
                pIndex = i

        if pIndex == -1:
            raise OrderException(msg='id为' + str(pid) + '的商品不存在，订单创建失败')
        else:
            product = products[pIndex]
            pStatus['id'] = product.id
            pStatus['count'] = number
            pStatus['name'] = product.name
            pStatus['p_total_price'] = str(product.price * number)
            pStatus['p_price'] = str(product.price)
            pStatus['main_image'] = product.main_image
            stock_ago = product.stock
            if product.stock < number:
                # pStatus['have_stock'] = False
                raise OrderException(msg='id为' + str(pid) + '的商品库存量不足，订单创建失败')
            with db.auto_commit():
                product.stock = product.stock - number
                db.session.add(product)
            FoodStockChangeLog.set_stock_change_log(product.id, stock_ago,
                                                    product.stock, '创建订单，减少库存')

        return pStatus

    def create_order_by_tran(self, data):
        """
        根据传入数据向订单表和订单商品表插入数据
        :param data:
        :return: 客户端需要的信息
        """
        try:
            with db.auto_commit():
                order = Order()
                order.order_sn = str(uuid1()).replace('-', '')
                order.member_id = self.member_id
                order.total_price = data['order_price']
                order.total_count = data['order_count']
                order.freight = Decimal('0.00')
                order.pay_price = order.total_price + order.freight
                order.snap_img = data['snap_img']
                order.snap_name = data['snap_name']
                order.snap_address = data['snap_address']
                order.snap_items = json.dumps(data['pStatusArray'])
                db.session.add(order)
                db.session.commit()

                foods = data['pStatusArray']
                for item in foods:
                    order_food = OrderFood()
                    order_food.order_id = order.id
                    order_food.food_id = item['id']
                    order_food.quantity = item['count']
                    order_food.total_price = Decimal(item['p_total_price'])
                    order_food.food_name = item['name']
                    order_food.food_img = item['main_image']
                    db.session.add(order_food)
        except Exception:
            raise OrderException(msg='下单失败请重新下单')
        return {
            'id': order.id,
            'order_sn': order.order_sn,
            'total_price': str(order.total_price)
        }

    @staticmethod
    def cancel_order(order):
        """
        取消订单: 还原商品库存, 订单状态改为已关闭
        :param order:
        :return:
        """
        if order.order_status_enum != OrderStatus.UNPAID:
            raise OrderException(msg='要取消订单，订单必须是未支付状态')
        order_foods = order.order_foods
        with db.auto_commit():
            for item in order_foods:
                food = item.food
                stock_ago = food.stock
                food.stock = food.stock + item.quantity
                item.remove()
                db.session.add(food)
                db.session.add(item)
                FoodStockChangeLog.set_stock_change_log(food.id, stock_ago, food.stock, '取消订单')

            order.order_status_enum = OrderStatus.CLOSE
            db.session.add(order)
        return Success(msg='取消订单成功')

    @staticmethod
    def confirm_order(order):
        with db.auto_commit():
            order.order_status_enum = OrderStatus.NOCOMMENT
            db.session.add(order)
        return Success(msg='确认已收货成功, 请给个简单评论吧')

    # @staticmethod
    # def get_order_sn():
    #     m = hashlib.md5()
    #     sn = None
    #     while True:
    #         str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
    #         m.update(str.encode("utf-8"))
    #         sn = m.hexdigest()
    #         if not Order.query.filter_by(order_sn=sn).first():
    #             break
    #     return sn
