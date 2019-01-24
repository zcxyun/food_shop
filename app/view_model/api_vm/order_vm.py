import json
from datetime import timedelta

from app.libs.utils import buildImageUrl
from app.view_model.base import BaseViewModel


class OrderViewModel(BaseViewModel):
    show_keys = ['name', 'status', 'status_desc', 'date', 'order_number', 'order_sn', 'note',
                 'pay_price', 'freight', 'total_price', 'address_dict', 'address_str',
                 'goods_list', 'deadline']

    def __init__(self, order):
        self.name = order.snap_name
        self.status = order.order_status
        self.status_desc = order.order_status_desc
        self.date = order.format_create_time
        self.order_number = order.order_number
        self.order_sn = order.order_sn
        self.note = order.note
        self.pay_price = str(order.pay_price)
        self.freight = str(order.freight)
        self.total_price = str(order.total_price)
        self.address_dict = json.loads(order.snap_address)
        self.address_str = self.set_address_info(self.address_dict)

        goods_list = json.loads(order.snap_items)
        for goods in goods_list:
            goods['main_image'] = buildImageUrl(goods['main_image'])
        self.goods_list = goods_list

        self.deadline = order.date_create_time + timedelta(minutes=30)

    def set_address_info(self, address):
        province = address['provinceName']
        city = address['cityName']
        county = address['countyName']
        detail = address['detailInfo']
        address_info = province + city + county + detail
        if self.is_center_city(province):
            address_info = city + county + detail
        return address_info

    @staticmethod
    def is_center_city(province):
        center_cities = ('北京市', '天津市', '上海市', '重庆市')
        return province in center_cities


class OrderCollection:

    @staticmethod
    def fill(orders):
        return [OrderViewModel(order) for order in orders]
