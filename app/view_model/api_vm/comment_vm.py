from app.view_model.base import BaseViewModel


class CommentViewModel(BaseViewModel):
    show_keys = ['score', 'date', 'content', 'user']

    def __init__(self, comment):
        member = comment.member
        self.score = comment.score_desc
        self.date = comment.format_create_time
        self.content = comment.content
        self.user = {
            'nickname': member.nickname,
            'avatar_url': member.avatar
        }


class CommentCollection:

    @staticmethod
    def fill(comments):
        return [CommentViewModel(comment) for comment in comments]


class MyCommentViewModel(BaseViewModel):

    def __init__(self, comment):
        self.date = comment.format_create_time
        self.content = comment.content
        self.order_number = comment.order.order_number


class MyCommentCollection:

    @staticmethod
    def fill(comments):
        return [MyCommentViewModel(comment) for comment in comments]
