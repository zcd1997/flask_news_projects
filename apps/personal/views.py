from flask import Blueprint, session, render_template, request, redirect, jsonify

from apps.home.models import User, Subscription, Classify
from db_ext import db

personal = Blueprint('personal', __name__)


@personal.route('/PersonCenter/')
def PersonCenter():
    subs = Subscription.query.filter(Subscription.is_sub == 1).all()
    if subs:
        for sub in subs:
            sub.classify = Classify.query.filter(Classify.c_id == sub.cid).all()

        return render_template('personal/index.html', subs=subs)
    else:
        return render_template('personal/index.html')


# 修改密码
@personal.route('/ChangePassword/', methods=['GET', 'POST'])
def ChangePassword():
    if request.method == 'GET':
        return render_template('personal/pp/possword.html')
    else:
        username = session['username']
        user = User.query.filter(User.username == username).first()
        if user:
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password != confirm_password:
                return "两次密码不一致!"
            user.password = password
            db.session.commit()
            session.clear()
            return redirect('/')
        else:
            return '该用户不存在'


# 修改邮箱
@personal.route('/ChangeEmail/', methods=['GET', 'POST'])
def ChangeEmail():
    if request.method == 'GET':
        return render_template('personal/pp/email.html')
    else:
        username = session['username']
        user = User.query.filter(User.username == username).first()
        if user:
            email = request.form['email']
            confirm_email = request.form['confirm_email']
            if email != confirm_email:
                return "两次邮箱不一致!"
            user.email = email
            db.session.commit()
            session.clear()
            return redirect('/')
        else:
            return '该用户不存在'


# 取消订阅
@personal.route('/Delete/', methods=['POST'])
def Delete():
    try:
        sub_id = request.values.get('sub_id')
        classify = Subscription.query.filter(Subscription.sub_id == sub_id).first()
        classify.is_sub = 0
        db.session.commit()
        data = {}
        data['status'] = 200
        data['msg'] = 'success'
        return jsonify(data)
        # return jsonify(result={'status': 200, 'msg': 'success', 'data': data})
    except:
        return jsonify(result={'status': 404, 'msg': 'failuer'})
