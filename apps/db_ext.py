# 数据库操作核心对象
import datetime

from flask import app
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# 　入口函数
def init_ext(app):
    init_db(app)
    init_cors(app)
    init_mail(app)


# ========数据库配置============
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    # 配置数据库连接
    config_db(app)
    db.init_app(app=app)
    migrate.init_app(app, db=db)


# 配置数据库的参数
def config_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@192.168.58.64:3306/flask_news'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 设置请求结束之后自动提交
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    SESSION_TYPE = 'redis'
    # 配置session的过期时间 默认浏览器关闭就失效
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)


# ========数据库配置ending========


# ========跨域请求配置==========

cors = CORS()


def init_cors(app):
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})


# =========跨域请求ending=======


# ========验证用户登录配置=======
# from flask_login import LoginManager
#
# lm = LoginManager()
#
#
# def init_login(app):
#     lm.login_view = '蓝图对象 登录的视图函数'
#     lm.init_app(app)


mail = Mail()


def init_mail(app):
    mail.init_app(app)


# ========用户登录ending==============
