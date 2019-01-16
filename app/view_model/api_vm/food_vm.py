from app.libs.utils import buildImageUrl
from app.view_model.base import BaseViewModel


class FoodViewModel(BaseViewModel):
    show_keys = ['id', 'name', 'summary', 'price', 'min_price', 'stock',
                 'total_count', 'comment_count', 'main_image', 'pic_url', 'pics']

    def __init__(self, food):
        self.id = food.id
        self.name = food.name
        self.summary = food.summary
        self.price = str(food.price)
        self.min_price = str(food.price)
        self.stock = food.stock

        self.total_count = food.total_count
        self.comment_count = food.comment_count

        self.main_image = buildImageUrl(food.main_image)
        self.pic_url = buildImageUrl(food.main_image)
        self.pics = [buildImageUrl(food.main_image)]


class FoodCollection:

    def fill(self, foods):
        return [FoodViewModel(food).show(
            'id', 'name', 'price', 'min_price', 'pic_url') for food in foods]
