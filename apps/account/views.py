import datetime
from functools import wraps
from io import BytesIO
from flask import Blueprint, request, render_template, session, redirect, url_for, make_response
from flask_mail import Message
from apps.db_ext import db, mail
from apps.home.models import User

account = Blueprint('account', __name__)


# 登录装饰器
def login_required(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('account.login', next=request.url))

    return __wrapper


# 验证码生成器
@account.route('/create_code/')
def create_code():
    from account.create_img_code import create_validate_code
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    session['img'] = strs.upper()
    return response


# 普通用户登录
@account.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        username = request.form['username']
        password = request.form['password']
        # 验证码转换大写
        yzm = request.form['yzm'].upper()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            if session['img'] != yzm:
                return "验证码错误!"
            if user.is_active == 0:
                return "该用户未被激活!"
            session['username'] = username
            return redirect('/')
        else:
            return '用户名或密码错误!'


# 管理员登录
@account.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('home/admin_login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username,
                                 User.password == password,
                                 User.is_superuser == 1).first()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return '管理员账户或密码错误!'


# 注册
@account.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('home/registration.html')
    else:
        username = request.form['username']
        if len(username) <= 8:
            return "用户名长度不符合规范"
        password = request.form['password']
        if len(password) < 6:
            return "密码长度不够!"
        confirm_pwd = request.form['confirm_pwd']
        if password != confirm_pwd:
            return '两次密码不一致!'
        email = request.form['email']
        create_date = datetime.datetime.now()
        user = User.query.filter_by(username=username).first()
        if user:
            return "该用户已被注册!"
        user = User(username=username,
                    password=password,
                    email=email,
                    create_date=create_date)
        db.session.add(user)

        try:
            # token = str(uuid.uuid4())
            active_url = 'http://127.0.0.1:8000/active_user/?username=%s' % username

            html = render_template('user_active.html', username=username, active_url=active_url)
            msg = Message(subject='激活账号邮件', body='全球最帅男子', sender='L15737628530@163.com',
                          recipients=[email, ], html=html)
            mail.send(msg)

            return '激活邮件已发送!'

        except Exception as e:
            print(e)
        return redirect('/')


# 　登出
@account.route('/login_out/')
def login_out():
    session.clear()
    return redirect('/')


# 邮箱激活
@account.route('/active_user/')
def ActiveUser():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()  # 注意这里边的first()
    if user:
        user.is_active = 1
        db.session.commit()

        return '激活成功!'
    else:
        return '激活失败!'
