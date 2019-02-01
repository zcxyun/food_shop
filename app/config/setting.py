DEBUG = True
ENV = 'development'

APP = {
    'domain': 'http://localhost:5000'
}

# TOKEN_EXPIRATION = 7200 * 12 * 30


# SEO_TITLE = "Python Flask构建微信小程序订餐系统"
##过滤url
# IGNORE_URLS = [
#     "^/user/login"
# ]
#
# IGNORE_CHECK_LOGIN_URLS = [
#     "^/static",
#     "^/favicon.ico"
# ]
#
# API_IGNORE_URLS = [
#     "^/api"
# ]

PAGE_SIZE = 5

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

SCORE_SELECT = {
    0: '差评',
    1: '一般',
    2: '好评'
}

MINA_APP = {
    'appid': 'wxfdcf36f2bf5d2af2',
    'appkey': '077c598d13e70592c6741f88c348b8b7',
    'paykey': '',
    'mch_id': '',
    'callback_url': '/api/order/callback',
    'page_size': 5
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_url': '/static/upload/'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "0": "待支付",
    "-1": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "-1": "订单关闭",
    "0": "待支付",
    "1": "支付成功",
    "2": "待发货",
    "3": "待确认",
    "4": "待评价"
}
