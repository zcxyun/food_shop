import json
from datetime import datetime, timedelta

import requests
from flask import current_app


def date_to_str(date=None, format='%Y-%m-%d %H:%M:%S'):
    if date is None:
        date = datetime.now()
    return date.strftime(format)


def now_timestamp():
    return int(datetime.now().timestamp())


def before_timestamp(days=30):
    timestamp = (datetime.now() - timedelta(days=days)).timestamp()
    return int(timestamp)


def get_openid(code):
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
        .format(current_app.config['MINA_APP']['appid'], current_app.config['MINA_APP']['appkey'], code)
    r = requests.get(url)
    res = json.loads(r.text)
    openid = None
    if 'openid' in res:
        openid = res['openid']
    return openid


def buildImageUrl(path):
    app_config = current_app.config['APP']
    url = app_config['domain'] + current_app.config['UPLOAD']['prefix_url'] + path
    return url
