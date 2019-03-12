# Flask and Flask-SQLAlchemy initialization here
from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView

from apps.home.models import User


class MyView(ModelView):
    # def is_accessible(self):
    #     return login.current_user.is_authenticated()
    # Disable model creation
    can_create = True

    column_labels = {
        'id': u'序号',
        'email': u'邮件',
        'username': u'用户名',
        'create_date': u'创建时间',
        'is_active': u'是否激活',
        'is_superuser': u'超级用户',
        'c_id': u'分类id',
        'c_name': u'分类名称',
        'view_count': u'浏览数量',
        'sub_count': u'订阅数量',
        'image_url': u'图片地址',
        'title': u'新闻标题',
        'content': u'内容',
        'news_date': u'新闻时间',
        'is_hot': u'是否热门',
    }
    column_exclude_list = ['password']


class NewsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/count.html')
