# -*- coding: utf-8 -*- 
import requests
import json

def download():
    #中国各省经纬度资料抓取
    url_api = "http://restapi.amap.com/v3/config/district"
    parameters = {'keywords': '中华人民共和国', 
                  'subdistrict': 2,
                  'key': 'ee83ffb0500bcbbe5929a0d58d012e0e'}
    r = requests.get (url_api, params=parameters)
    data = r.json()

    ans09 ={ x['name']: [y['name'] for y in x['districts']] for x in data['districts'][0]['districts'] }
    l = [[kk+x for x in ll] for kk,ll in ans09.items()]
    F=[y for sublist in l for y in sublist]
    ans10 ={ x['name']: [y['center'] for y in x['districts']] for x in data['districts'][0]['districts']}
    R=ans10.values()
    Z=list(R)
    T=[y for x in Z for y in x]
    _cities={}
    for i in range(len(F)):
        _cities[F[i]]=T[i]
    return(_cities)
    

    
try:
    with open('data/chinesemap.json','r') as fp:
        PRC_cities = json.load(fp)
except:
    PRC_cities = download()
    with open('data/chinesemap.json','w') as file:
        json.dump(PRC_cities, file)


  
#抓取地图
def get_img(a_city, z='10'):
    path_img = "maps/{img}_{zo}.png".format(img=a_city, zo=z)
    #高德地图（静态地图）api
    url_api = "http://restapi.amap.com/v3/staticmap"
    parameters={'location':'',
                'zoom':z,
                'size':'1000*600',
                'key': 'ee83ffb0500bcbbe5929a0d58d012e0e'}
    
    parameters['location']= PRC_cities[a_city]
    r = requests.get(url_api, params=parameters)
    try:
        data = r.json()
    except:
        data = r.content
    with open (path_img, "wb") as f:
        f.write(r.content)
    return path_img


