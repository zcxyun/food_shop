from enum import Enum


class OrderStatus(Enum):
    UNPAID = 0  # 待支付
    PAID = 1  # 已支付(待发货)
    DELIVERED = 2  # 已发货(待收货)
    NOCOMMENT = 3  # 待评论
    DONE = 4  # 已完成(已评论)
    CLOSE = -1  # 交易关闭


class ClientType(Enum):
    WECHAT = 1
