from flask import Blueprint, request, jsonify, render_template

from apps.home.models import News, Classify

count = Blueprint('count', __name__)


@count.route('/admin/newcount/', methods=['POST', 'GET'])
def news_count():
    if request.method == 'GET':
        data = {}
        title = []
        count = []
        news = News.query.order_by(News.classify_id).limit(7).all()
        for new in news:
            title.append(new.classify_id)
            count.append(new.view_count)
        data['title'] = title
        data['count'] = count
        return render_template('admin/news_count.html', data=data)


@count.route('/admin/leibiecount/', methods=['POST', 'GET'])
def leibie_count():
    if request.method == 'GET':
        data = {}
        title = []
        count = []
        leibies = Classify.query.order_by(Classify.c_id).all()
        for leibie in leibies:
            title.append(leibie.c_name)
            count.append(leibie.view_count)
        data['title'] = title
        data['count'] = count
        return render_template('admin/leibie_count.html', data=data)


@count.route('/admin/yudingcount/', methods=['POST', 'GET'])
def yuding_count():
    if request.method == 'GET':
        data = {}
        title = []
        count = []
        leibies = Classify.query.order_by(Classify.c_id).all()
        for leibie in leibies:
            title.append(leibie.c_name)
            count.append(leibie.sub_count)
        data['title'] = title
        data['count'] = count
        return render_template('admin/yuding_count.html', data=data)
