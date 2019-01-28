from flask_script import Manager, Server
from food_shop import app

from flask_migrate import Migrate, MigrateCommand
from app.models import db
from app.jobs.pay import pay
from app.jobs.queue import queue
from app.jobs.stat import stat

manager = Manager(app)

# init  migrate upgrade
# 模型 -> 迁移文件 -> 表
# 1.要使用flask_migrate,必须绑定app和DB
migrate = Migrate(app, db)

# 2.把migrateCommand命令添加到manager中。
manager.add_command('db', MigrateCommand)
# 关闭超过30分钟未支付的订单
manager.add_command('pay', pay)
# 通过队列形式发送模板消息，并更新相应产品的销售数据
manager.add_command('queue', queue)
# 统计会员，产品，全站每日数据
manager.add_command('stat', stat)

# manager.add_command('runserver', Server(host='localhost', port=5000, use_debugger=True, use_reloader=True))

if __name__ == '__main__':
    manager.run()
