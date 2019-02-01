from enum import Enum


class Status(Enum):
    """
    表字段状态
    """
    EXIST = 1
    DELETED = 0


class OrderStatus(Enum):
    """
    订单状态
    """
    UNPAID = 0  # 待支付
    PAID = 1  # 已支付(待发货)
    DELIVERED = 2  # 已发货(待收货)
    NOCOMMENT = 3  # 待评论
    DONE = 4  # 已完成(已评论)
    CLOSE = -1  # 交易关闭


class ClientType(Enum):
    """
    客户端类型
    """
    WECHAT = 1


class QueueHandleStatus(Enum):
    """
    模板消息队列处理情况
    """
    UNPROCESSED = 0
    PROCESSED = 1


class Score(Enum):
    """
    会员评分
    """
    LOW = 0
    MID = 1
    HIGH = 2
