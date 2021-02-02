from flask import Flask
from flask import render_template
from flask import request,make_response,redirect
import sqlSearch
import fenye

app = Flask(__name__)

@app.route('/fang')
def index():
    isLogin = request.cookies.get('username') == 'admin'
    if isLogin:
        p = request.args.get("p")
        if p:
            my_list = sqlSearch.search(int(p))
            fen = fenye.main(int(p))
            return render_template(
                # 渲染模板语言
                'test.html',
                my_list=my_list,
                fen=fen
            )
        else:
            my_list = sqlSearch.search(1)
            fen = fenye.main(1)
            return render_template(
                # 渲染模板语言
                'test.html',
                my_list=my_list,
                fen=fen
            )
    else:
        return redirect('/')

@app.route('/tu')
def showTu():
    isLogin = request.cookies.get('username') == 'admin'
    if isLogin:
        zhuTu = '/static/img/广州房价.png'
        binTu = '/static/img/广州商品房房龄分布.png'
        return render_template(
            # 渲染模板语言
            'tu.html',
            zhuTu=zhuTu,
            binTu=binTu
        )
    else:
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def isLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':

            resp = make_response(redirect('/tu'))
            resp.set_cookie('username', username)

            return resp
        else:
            return '用户名或密码错误！'

    return render_template('login.html')


if __name__ == '__main__':
    app.run()