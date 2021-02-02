#-*- coding=utf-8 -*-#
from flask import Flask, render_template, request, escape,flash

import json, urllib
from urllib import parse
from vsearch import search4letters

app = Flask(__name__)
appKey="a6e4ba9c7b179bc9fce32fdd92a44114"
app.secret_key = '520'
import requests
def get_xzpd(men,women):
    key = "2aaf134d4a120511d74719d01e8eaff9"
    payload = {
    'men': men,
    'women': women,
    'key':key
        
    }
    req = requests.get('http://apis.juhe.cn/xzpd/query', params=payload)
    return req.json()["result"]


def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results."""
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

@app.route('/jieguo', methods=['POST'])
def do_search():
    """Extract the posted data; perform the search; return results."""
    men = request.form['men']
    women = request.form['women']

    print(men,women)
    title = 'Here are your results:'
    # if not parse:
    #     return None
    try:
        results = get_xzpd(men,women)
        print(results)
        # content = []
        # titles = []
        # if results:
        #     for i in results:
        #         titles.append(i)
        # print(titles)
        # for i in titles:
        #      content.append(escape(results["{}".format(i)]))
        # print(content)
        name_1 = "{}".format(results['men']),
        datatime_1 = str(results['women']),
        all_1 = str(results['zhishu']),
        QFriend_1 = str(results['bizhong']),
        color_1= str(results['jieguo']),
        number_1 = str(results['lianai']),
        summary_1 = str(results['zhuyi']),
        if name_1:
                
            # titles = ('id地址','主要内容','详细信息')
            log_request(request, results)
            return render_template('jieguo.html',
                                   the_title=u'    哒哒哒~您的匹配如下',
                                   name = name_1[0],
                                   datatime = datatime_1[0],
                                   all = all_1[0],
                                   QFriend = QFriend_1[0],
                                   color= color_1[0],
                                   number = number_1[0],
                                   summary =  summary_1[0],

                                   )
        else:
            return render_template('jieguo.html',
                                   the_title=u'    哒哒哒~您的匹配如下',
                                   name = "您的匹配出错请返回重新匹配"
                                  

                                   )
    except:
        return render_template('jieguo.html',
                                   the_title=u'    哒哒哒~您的匹配如下',
                                   name = "您的匹配出错请返回重新匹配"
                                  

                                   )
        


                               # the_row_titles=titles,
                           # the_data=content)
## 日志系统



@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login',methods =['POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash("username empty")
            return  render_template('login.html')
        if not password:
            flash('password empty')
            return render_template('login.html')

        account =[];
        with open('user.txt','r') as r:
            data = r.readlines()

        if not data:
            flash('user empty')
            return  render_template('register.html')
        print(account)
        for i in data:
            account.append(i.strip('\n').strip('\r\n'))
        flag =False
        if not account:
            flash('user empty')
            return render_template('register.html')
        for i in account:

            splitData= i.split(':')
            print(splitData)
            print(splitData[0])
            print('username')
            print(username)
            if  splitData:
                if username == splitData[0] and password ==splitData[1]:
                    print('xxx')
                    flag=True
                    break

        print(flag)
        print('flag')
        if  not flag:
            flash('username or password error')
            return render_template('login.html')

        return render_template('lists.html')

@app.route('/register',methods =['GET','POST'])
def register():
    if request.method =='GET':
        return render_template('register.html')
    elif request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash("username empty")
            return render_template('register.html')
        if not password:
            flash('password empty')
            return render_template('register.html')

        with open('user.txt','a+') as f:
            f.write(username+":"+password+"\n")
        return render_template('login.html')

@app.route('/gongneng',methods=['GET','POST'])
def view_the_log():
    """Display the contents of the log file as a HTML table."""
    contents = []
    with open('content.txt.log','r', encoding='UTF-8') as f:
        result =f.readlines()
    # if not result:
    #     result=request1(appKey,'GET')
    #     print(result)
    #     if result:
    #         with open('content.txt','a+') as f :
    #             for i in result:
    #                 f.write(i.get('name')+'\n')
    if result:
        for line in result:
            line=line.strip('\n').strip('\r\n')
            contents.append(line)
    titles = ('fid', 'id', 'name')
    return render_template('gongneng.html',
                           the_title='祝你好运！--快来看看你的星座每日运势吧',
                           the_title2='type',
                           the_row_titles=titles,
                           the_data=contents,)
@app.route('/detail')
def detail():
    parems = request.args
    print(parems.get('id'))
    id = parems.get('id')
    result= request3(appKey,id,"GET")
    data =None
    if result:
        data=result
    return render_template('detail.html',data=data)



## 日志系统
@app.route('/rizi')
def showlog() -> 'html':
    """Display the contents of the log file as a HTML table."""
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    print(contents[0])
    return render_template('rizi.html',
                           the_title='日志查询系统',
                           the_row_titles=titles,
                           the_data=contents)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8082,debug=True)
