from flask_admin import Admin
from flask_babelex import Babel
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from admin.admin_view import MyView, NewsView
from apps import create_app
from db_ext import db
from apps.home.models import User, News, Classify

app = create_app()
manage = Manager(app)

app.config['SECRET_KEY'] = '123456'
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
admin = Admin(app, name='BBC新闻后台管理系统')
admin.add_view(MyView(User, db.session, name='用户'))
admin.add_view(MyView(News, db.session, name='新闻'))
admin.add_view(MyView(Classify, db.session, name='新闻类别'))
admin.add_view(NewsView(name='统计'))

manage.add_command('run', Server(port=8000))  # 多线程
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()
