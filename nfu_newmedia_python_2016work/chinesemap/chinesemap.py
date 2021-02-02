# -*- coding: utf-8 -*- 
from flask import Flask, render_template, request, escape, url_for, send_file
from lookup_longitude_latitude import get_img

app = Flask(__name__)

import json
with open('data/PRCmap.json','rb')as fp:
    python=json.load(fp)
cities=python.keys()
city_list=list(cities)

@app.route('/pick_city', methods=['POST'])
def do_search() -> 'html':
    """Extract the posted data; perform the search; return results."""
    user_city = request.form['the_user_city']
    title = '以下是您的结果：'
    results = []
    zoom_list=list(range(7,14,3))
    for y in zoom_list:
        results.append( get_img(user_city, z=y) )
    results = {zoom_list[i]:x for i,x in enumerate(results)}
    return render_template('results.html',
                           the_title=title,
                           the_city=user_city,
                           the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Display this webapp's HTML form."""
    print(city_list)
    return render_template('entry.html',
                           the_title='城市地图导航',
                           the_available_city=city_list)



#这里我们接受一个 filename 檔名变量，http://127.0.0.1:5000/img/檔名
@app.route('/maps/<filename>')  #filename
def get_image(filename):        #filename 
    #傳送mimetype="image/"
    #假定都是image/png格式
    import os.path
    
    return send_file(os.path.join("maps",filename), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
