chinesemap

英文项目名称chinesemap
		
# 简介 
选取城市得到相对应的城市地图，输入方面用户选取城市名称，输出方面则是输出3张不同比例的城市地图，可查394个国内城市，数据来源高德地图API数据抓取的json档。
		
## 输入：

用户输入城市，交互界面使用到[HTML5之datalist标签](http://www.w3school.com.cn/html5/html5_datalist.asp)，显示的是 城市名称 ，所以用户可以用 城市名称 找所需要的城市地图。

## 输出：

用户得到输出结果为：3张不同比例的城市地图，见[tempaltes/results.html](tempaltes/results.html)

## 从输入到输出，本组作品使用了：
### 模块
* requests(http://www.python-requests.org/en/master/)
* json(http://www.runoob.com/json/json-tutorial.html)

### 数据
* [高德地图行政区域查询](http://restapi.amap.com/v3/config/district?key=ee83ffb0500bcbbe5929a0d58d012e0e&keywords=中国&subdistrict=2&showbiz=fa)

### API
* [高德地图行政区域查询API](http://restapi.amap.com/v3/config/district)
* [高德地图静态地图API](http://restapi.amap.com/v3/staticmap)


## Web App动作描述

以下按web 请求（web request） - web 响应 时序说明

1. 後端伺服器启动：执行 chinesemap.py 启动後端伺服器，等待web 请求。启动成功应出现：  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

2. 前端浏览器web 请求：访问 http://127.0.0.1:5000/ 启动前端web 请求

3. 後端伺服器web 响应：[chinesemap.py](chinesemap.py) 中 执行 了@app.route('/') 下的 entry_page()函数，以HTML模版[templates/entry.html](templates/entry.html)及一个含城市名称的列表（见代码 the_available_city=city_list）产出的产生《城市地图导航》的HTML页面

4. 前端浏览器收到web 响应：出现HTML页面有HTML表单的输入 input 类型(type) 为"text"，变数名称(name)为'the_user_city'，使用了HTML5的datalist 定义在 list="city" 及 datalist标签，详见HTML模版[templates/entry.html](templates/entry.html)

5. 前端浏览器web 请求：用户选取指标後按了提交钮「搜寻」，则产生新的web 请求，按照form元素中定义的method='POST' action='/pick_city'，以POST为方法，动作为/pick_city的web 请求

6. 後端服务器收到用户web 请求，匹配到@app.route('/pick_city', methods=['POST'])的函数 do_search() 

7. [chinesemap.py](chinesemap.py) 中 def do_search() 函数，把用户提交的数据，以flask 模块request.form['the_user_city']	取到Web 请求中，HTML表单变数名称the_user_city的值，存放在user_city这Python变数下，再使用flask模块render_template 函数以[templates/results.html](templates/results.html)模版为基础（输出），其中模版中the_city的值，用user_city这变数之值，其他1项值如此类推。

8. 前端浏览器收到web 响应：模版中[templates/results.html](templates/results.html) 的变数值正确的产生的话，前端浏览器会收到正确响应，看到相关的3张不同比例的城市地图。

## 作者成员：
见[_team_.tsv](_team_/_team_.tsv)

