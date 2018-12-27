from datetime import datetime, timedelta


def date_to_str(date=None, format='%Y-%m-%d %H:%M:%S'):
    if date is None:
        date = datetime.now()
    return date.strftime(format)


def now_timestamp():
    return int(datetime.now().timestamp())


def before_timestamp(days=30):
    timestamp = (datetime.now() - timedelta(days=days)).timestamp()
    return int(timestamp)


