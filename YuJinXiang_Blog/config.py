class BaseConfig:
    SECRET_KEY = "zyssj"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PER_PAGE_COUNT = 10


class DevelopmentConfig(BaseConfig):
    # MySql配置
    HOSTNAME = 'localhost'
    PORT = '3306'
    DATABASE = 'yujinxiang_blog'
    USERNAME = 'root'
    PASSWORD = 'root'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'\
        .format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "2337051839@qq.com"
    MAIL_PASSWORD = "iwkgntahvyigdibb"
    MAIL_DEFAULT_SENDER = "2337051839@qq.com"

    # Redis配置

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = "6379"
