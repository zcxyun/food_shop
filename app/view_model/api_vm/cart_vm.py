from app.libs.utils import buildImageUrl
from app.view_model.base import BaseViewModel


class CartViewModel(BaseViewModel):
    show_keys = ['id', 'number', 'stock', 'food_id', 'name', 'price', 'pic_url', 'active']

    def __init__(self, cart):
        food = cart.food
        self.id = cart.id
        self.number = cart.quantity
        self.stock = food.stock
        self.food_id = cart.food_id
        self.name = food.name
        self.price = str(food.price)
        self.pic_url = buildImageUrl(food.main_image)
        self.active = True


class CartCollection:

    def fill(self, cart_list):
        return [CartViewModel(cart) for cart in cart_list]
