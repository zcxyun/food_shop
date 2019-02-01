from app.view_model.base import BaseViewModel


class CommentViewModel(BaseViewModel):
    show_keys = ('score', 'content', 'member_info', 'foods_str')

    def __init__(self, comment):
        self.score = comment.score_desc
        self.content = comment.content
        self.member_info = comment.member
        foods = comment.order.foods
        foods_str = ', '.join([food.name for food in foods])
        self.foods_str = foods_str


class CommentCollection:

    @staticmethod
    def fill(comments):
        return [CommentViewModel(comment) for comment in comments]
