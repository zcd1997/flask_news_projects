import flask_whooshalchemyplus
from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from apps.home.models import News, Classify, User, Subscription
from db_ext import db

home = Blueprint('home', __name__, template_folder='templates')


# 　首页
@home.route('/')
def index():
    categorys = Classify.query.filter().all()
    banners_list = News.query.filter().limit(4).all()
    news_left = News.query.filter().limit(3).offset(41).all()
    news_right = News.query.filter().limit(3).offset(59).all()
    news = News.query.filter().all()
    hot_news = News.query.filter_by(is_hot=1).limit(6).all()
    return render_template('index.html', categorys=categorys, banners_list=banners_list, news_left=news_left,
                           news_right=news_right, news=news, hot_news=hot_news, dets=news)


#   分类页面
# @login_required   登录装饰器
@home.route('/cart/<int:c_id>/<int:page>')
def cart(c_id, page):
    if not page:
        page = 1
    categorys = Classify.query.filter().all()
    news_classify = Classify.query.filter(Classify.c_id == c_id).all()[0]
    news = News.query.filter_by(classify_id=c_id).paginate(page=page, per_page=6)
    hot_news = News.query.filter_by(is_hot=1, classify_id=c_id).limit(6).all()

    news_classify.view_count += 1
    db.session.commit()
    if session.get('username'):
        user = User.query.filter(User.username == session.get('username')).first()
        sub = Subscription.query.filter(Subscription.uid == user.user_id, Subscription.cid == c_id).first()
        return render_template('cart.html', news=news.items, classify=news_classify,
                               dets=news, categorys=categorys, user=user, sub=sub, hot_news=hot_news)
        # if session['username'] != None:
        #     sess_name = session['username']
        #     user = User.query.filter(User.username == sess_name).first()
        #     sub = Subscription.query.filter(Subscription.uid == user.user_id, Subscription.cid == c_id).first()
        #
        #     return render_template('cart.html', news=news.items, classify=news_classify,
        #                        dets=news, categorys=categorys, user=user, sub=sub)
    else:
        return render_template('cart.html', news=news.items, classify=news_classify,
                               dets=news, categorys=categorys, hot_news=hot_news)


#   详情页面
@home.route('/detail/<new_id>')
def detail(new_id):
    categorys = Classify.query.filter().all()
    new = News.query.filter(News.new_id == new_id).all()[0]
    new.view_count += 1
    db.session.commit()
    return render_template('home/detail.html', new=new, categorys=categorys)


@home.route('/sub_no', methods=['GET', 'POST'])
def sub_no():
    sess_name = session['username']
    c_id = request.args.get('cate_id')
    user = User.query.filter(User.username == sess_name).first()
    sub = Subscription.query.filter(Subscription.uid == user.user_id, Subscription.cid == c_id).first()
    if sub:
        sub.is_sub = 0
        db.session.commit()
        data = {}
        data['status'] = 200
        data['msg'] = 'success'
        return jsonify(data)


@home.route('/sub_yes', methods=['GET', 'POST'])
def sub_yes():
    sess_name = session['username']
    c_id = request.args.get('cate_id')
    user = User.query.filter(User.username == sess_name).first()
    sub = Subscription.query.filter(Subscription.uid == user.user_id, Subscription.cid == c_id).first()
    if sub:
        sub.is_sub = 1
        db.session.commit()
        data = {}
        data['status'] = 200
        data['msg'] = 'success'
        return jsonify(data)
    else:
        sub = Subscription(is_sub=1, uid=user.user_id, cid=c_id)
        db.session.add(sub)
        data = {}
        data['status'] = 200
        data['msg'] = 'success'
        return jsonify(data)


# 搜索功能
@home.route('/search', methods=['POST'])
def search():
    if not request.form['search']:
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=request.form['search']))


# 搜索结果
@home.route('/search_results/<query>')
def search_results(query):
    flask_whooshalchemyplus.index_one_model(News)

    results = News.query.whoosh_search(query).all()
    return render_template('search/search.html', query=query, results=results)
