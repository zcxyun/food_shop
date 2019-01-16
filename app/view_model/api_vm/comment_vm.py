from app.view_model.base import BaseViewModel


class CommentViewModel(BaseViewModel):
    show_keys = ['score', 'date', 'content', 'user']

    def __init__(self, comment):
        self.score = comment.score_desc
        self.date = comment.format_create_time
        self.content = comment.content
        self.user = {
            'nickname': comment.member.nickname,
            'avatar_url': comment.member.avatar
        }


class CommentCollection:

    def fill(self, comments):
        return [CommentViewModel(comment) for comment in comments]
