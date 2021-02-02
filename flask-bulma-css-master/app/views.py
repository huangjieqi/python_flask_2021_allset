# -*- encoding: utf-8 -*-
"""
Flask Bulma CSS Starter
Author: AppSeed.us - App Generator 
"""
import datetime
import requests
from bs4 import BeautifulSoup
# all the imports necessary
from flask import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os
import json
from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm

import os, shutil, re, cgi



def get_dictum_info():
    """
    获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
    :return: str， 一句格言或者短语。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36',
    }
#     print('获取格言信息...')
    user_url = 'http://wufazhuce.com/'
    resp = requests.get(user_url, headers=headers)
    if resp.status_code == 200:
        soup_texts = BeautifulSoup(resp.text, 'lxml')
        # 『one -个』 中的每日一句
        every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
        return every_msg + '\n'
    print('每日一句获取失败。')
    return None

def get_weather(city="广州"):
    """调用api获取天气数据"""
    key = "97d3ae7d1e1209220b6e0114a070b64e"
    payload = {
    'cityname': city,
    'dtype': 'json',
    'format': 1,
    'key':key
        
    }
    req = requests.get('http://v.juhe.cn/weather/index', params=payload)
    return req.json()        
# provide login manager with load_user callback



def weather_str(data_weather):
    tianqi_dict = {"城市":data_weather['result']["today"]['city'],
    "今日温度":data_weather['result']["today"]['temperature'],
     "今日天气":data_weather['result']["today"]['weather'],
     "风向":data_weather['result']["today"]['wind'],
     "穿衣指数":data_weather['result']["today"]['dressing_index'],
     "穿衣建议":data_weather['result']["today"]['dressing_advice'],
    }
    print_msg = (
        
    ' 📍 您好，现在是北京时间{hour}点{minute}分，您所在的城市为{city}，今天的天气为{weather},\
    温度为{temperature}，伴有{wind}，天气{dressing_index},{dressing_advice}\n'.format(\
        city=tianqi_dict["城市"],weather=tianqi_dict["今日天气"],temperature=tianqi_dict["今日温度"],\
        wind=tianqi_dict["风向"],dressing_index=tianqi_dict["穿衣指数"],dressing_advice=tianqi_dict["穿衣建议"],\
        hour=datetime.datetime.now().hour,minute=datetime.datetime.now().minute))

    return print_msg

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # define login form here
    form = RegisterForm(request.form)

    msg = None

    # custommize your pate title / description here
    page_title       = 'Register - Flask Bulma CSS App | AppSeed App Generator'
    page_description = 'Open-Source Flask, Bulma CSS stater, the registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        name     = request.form.get('name'    , '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:                    
            pw_hash = bc.generate_password_hash(password)

            user = User(username, pw_hash, name, email)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    # try to match the pages defined in -> themes/phantom/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/register.html', form=form, msg=msg) )

# authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # define login form here
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # custommize your page title / description here
    page_title       = 'Login - Flask Bulma CSS App | AppSeed App Generator'
    page_description = 'Open-Source Flask, Bulma CSS stater, the login page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    # try to match the pages defined in -> themes/phantom/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/login.html', 
                                                     form=form,
                                                     msg=msg) )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    content = None

    try:

        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )

    except:
        abort(404)

# api模块
# 每日格言
@app.route("/api_mrgy", methods=['GET', 'POST'])
def api_mrgy():
    data = get_dictum_info()
    return jsonify({"msg": data})
# 每日天气
@app.route("/api_weather", methods=['GET', 'POST'])
def api_weather():
    data = get_weather()
    return data #jsonify({"msg": data})
# 每日天气定制化
@app.route("/mrtq", methods=['GET', 'POST'])
def mrtq():
    
    p_name = request.form["name"]
    sex = request.form["sex"]
    city = request.form["city"]
    if sex == '男':
        # print('男')
        msg = weather_str(data_weather=get_weather(city = city))
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+'form-mrtq.html',msg=msg,name= p_name+"先生") )



    elif sex == '女':
        msg = weather_str(data_weather=get_weather(city = city))
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+'form-mrtq.html',msg=msg,name= p_name+"女士") )


    print(name,sex,city)
    # data = get_dictum_info()

    # return jsonify({"msg": data})

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@app.route('/sitemap.xml')
#def sitemap():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'sitemap.xml')

#@app.route('/googlee35aa2f2fd798797985b.html')
#def google_checker():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'googlee35aa2f2fd__YOUR_GOOGLE_HTML__.html')

# ------------------------------------------------------

# error handling
# most common error codes have been added for now
# TO DO:
# they could use some styling so they don't look so ugly

def http_err(err_code):
	
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
	
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in themes/phantom/pages"
    
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
    
@app.errorhandler(401)
def e401(e):
    return http_err( 401) # "It seems like you are not allowed to access this link."

@app.errorhandler(404)
def e404(e):
    return http_err( 404) # "The URL you were looking for does not seem to exist.<br><br>
	                      # If you have typed the link manually, make sure you've spelled the link right."

@app.errorhandler(500)
def e500(e):
    return http_err( 500) # "Internal error. Contact the manager about this."

@app.errorhandler(403)
def e403(e):
    return http_err( 403 ) # "Forbidden access."

@app.errorhandler(410)
def e410(e):
    return http_err( 410) # "The content you were looking for has been deleted."

	