DIALECT = 'mysql'           # 要用的什么数据库
DRIVER = 'cymysql'          # 连接数据库驱动
USERNAME = 'root'           # 用户名
PASSWORD = 'zhaolong'       # 密码
HOST = 'localhost'          # 服务器
PORT = '3306'               # 端口
DATABASE = 'food_shop'      # 数据库名

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:zhaolong@localhost:3306/food_shop'
# SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'
