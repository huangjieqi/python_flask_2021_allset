# 从flask库中导入Flask类
from flask import Flask
# 导入模板方法
from flask import render_template
# 导入请求方法，响应方法，重定向
from flask import request,make_response,redirect

# 我们自己写的其他函数
from searchSql import searchPassword,addUser,search
import json

# 新建一个Flask服务器
app = Flask(__name__)

# 门牌号，这个门牌号就是/  当有外人访问你家时  就通过这个门牌号去找到你家
# get  post
@app.route('/', methods=['GET', 'POST'])
def isLogin():
    # 先判断下 用户现在是要登录还是访问网页
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sqlPassword = searchPassword(username)

        if username and password and sqlPassword and sqlPassword == password:
            resp = make_response(redirect('/weather'))
            resp.set_cookie('username', username)
            # return resp
            return resp
        else:
            return '用户名或密码错误！'


    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = json.loads(request.data)['username']
        password = json.loads(request.data)['password']
        sqlPassword = searchPassword(username)
        if sqlPassword:
            return json.dumps({'msg':'用户名存在'})
        else:
            result = addUser(username,password)
            if result:
                return json.dumps({'msg':'注册成功'})
            else:
                return json.dumps({'msg':'注册失败'})


    return render_template('register.html')

@app.route('/weather')
def showWeather():
    username = request.cookies.get('username')
    sqlPassword = searchPassword(username)

    if sqlPassword:
        dataList = search()
        return render_template('weather.html',dataList=dataList)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run()