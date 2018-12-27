from app.view_model.base import BaseViewModel


class IndexViewModel(BaseViewModel):
    data = {
        'finance': {
            'today': 0,
            'month': 0
        },
        'member': {
            'today_new': 0,
            'month_new': 0,
            'total': 0
        },
        'order': {
            'today': 0,
            'month': 0
        },
        'shared': {
            'today': 0,
            'month': 0
        },
    }