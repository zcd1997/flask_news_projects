from flask import Flask
from admin.admin_count import count
from apps.account.views import account
from apps.db_ext import init_ext
from apps.home.views import home
from apps.personal.views import personal
import flask_whooshalchemyplus


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123456'  # 用于保存session的
    '''
    邮箱激活相关配置!
    '''
    app.config['MAIL_DEBUG'] = True
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'L15737628530@163.com'
    app.config['MAIL_PASSWORD'] = 'lixin123'
    app.debug = True  # 注意产品上线的时候要管了
    register_blue(app)  # 注册蓝图对象
    init_ext(app)  # 数据库相关 拓展程序
    # 全文检索
    flask_whooshalchemyplus.init_app(app)
    return app


# 注册蓝图对象
def register_blue(app):
    # 首页模块　分类　详情
    app.register_blueprint(home)
    # 　登录注册模块
    app.register_blueprint(account)
    #  个人中心  订阅
    app.register_blueprint(personal)
    # 后台管理界面
    app.register_blueprint(count)
