from app.libs.utils import buildImageUrl
from app.models import Food
from decimal import Decimal


class OrderService:

    def __init__(self, goods):
        self.food_dic = {good['id']: good['number'] for good in goods}
        self.food_list = Food.query.filter(
            Food.id.in_(self.food_dic.keys()), Food.status == 1).all()

    def get_order(self):
        pay_price = freight = Decimal(0.00)
        data_food_list = []
        for item in self.food_list:
            tmp_data = self._deal_data(item)
            data_food_list.append(tmp_data)
            pay_price += item.price * self.food_dic[item.id]

        return data_food_list, pay_price, freight

    def _deal_data(self, data):
        return {
            'id': data.id,
            'name': data.name,
            'price': str(data.price),
            'pic_url': buildImageUrl(data.main_image),
            'number': self.food_dic[data.id]
        }