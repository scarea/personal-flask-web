from flask import Flask, render_template, request, redirect
import pymysql
import jwt
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'awen'
try:
    # 建立数据库连接
    conn = pymysql.connect(
    host='127.0.0.1',     # 数据库主机地址
    user='root',          # 数据库用户名
    password='******',    # 数据库密码
    db='flask_test'       # 数据库名称
)
    print("数据库成功连接")
except pymysql.Error as e:
    print("数据库连接失败")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        # 连接到数据库
        cursor = conn.cursor()

        # 执行数据库查询
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))

        # 获取查询结果
        user = cursor.fetchone()

        # 关闭数据库连接
        cursor.close()
        conn.close()

        # 检查用户是否存在且密码正确
        if user and user[1] == password:
            # 创建 JWT
            token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
            # 重定向到成功页面，并将 JWT 作为参数传递
            print('登录成功：')
            return redirect('/success?token='+token)
        else:
            # 重定向到失败页面
            return redirect('/fail')

    return render_template('login.html')


# 定义需要进行权限认证的接口
@app.route('/success')
def success():
    # 从请求中获取 JWT 令牌
    token = request.args.get('token')

    try:
        # 验证 JWT 令牌
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = decoded['username']
        # 在这里可以进行相应的权限验证和业务逻辑处理
        return 'Login successful! Welcome, ' + username
    except jwt.DecodeError:
        return 'Invalid token'
    except jwt.ExpiredSignatureError:
        return 'Token expired'


@app.route('/fail')
def fail():
    return render_template('fail.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(1)
        username = request.json['username']
        password = request.json['password']
        print(username)
        print(password)
        # 在此处执行注册逻辑
        # 可以使用MySQL连接执行相关插入操作

        return 'Registered successfully!'
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
