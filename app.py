from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('1')
        print(request.json)
        username = request.json['username']
        password = request.json['password']
        print(username)
        print(password)
        # 在此处执行登录验证逻辑
        # 可以使用MySQL连接执行相关查询等操作

        return 'Logged in successfully!'
    return render_template('login.html')

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
