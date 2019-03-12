import datetime

from jieba.analyse import ChineseAnalyzer

from apps.db_ext import db


# 用户表
class User(db.Model):
    # 用户id
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    # 密码
    password = db.Column(db.String(100), nullable=False)
    # 邮箱
    email = db.Column(db.String(100))
    # 创建用户时间
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    # 是否激活(邮箱激活)
    is_active = db.Column(db.Integer, default=0)
    # 是否超级管理员
    is_superuser = db.Column(db.Integer, default=0)


# 新闻分类表
class Classify(db.Model):
    # 分类id
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 分类名称
    c_name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    # 浏览数量
    view_count = db.Column(db.Integer, default=0)
    # 订阅数量
    sub_count = db.Column(db.Integer, default=0)


# 新闻表
class News(db.Model):
    # 新闻id
    new_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 新闻图片地址
    image_url = db.Column(db.String(300))
    # 新闻标题
    title = db.Column(db.String(100), index=True, nullable=False)
    # 内容(url,主要内容在mongdb)
    content = db.Column(db.String(100), nullable=False)
    # 新闻时间
    news_date = db.Column(db.String(64), nullable=False)
    # 浏览数量
    view_count = db.Column(db.Integer, default=0)
    # 是否热门新闻
    is_hot = db.Column(db.Integer, default=0)
    # 关联分类表,所属类别
    classify_id = db.Column(db.Integer, db.ForeignKey(Classify.c_id))
    # 全文检索配置
    __searchable__ = ['content', 'title']
    __analyzer__ = ChineseAnalyzer()


# 　订阅表
class Subscription(db.Model):
    # 订阅id
    sub_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 是否订阅(主要用于取消订阅)
    is_sub = db.Column(db.Integer, default=0)
    # 关联用户id
    uid = db.Column(db.Integer, db.ForeignKey(User.user_id))
    # 关联分类id
    cid = db.Column(db.Integer, db.ForeignKey(Classify.c_id))
