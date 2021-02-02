#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import parse
from urllib import request

# ----------------------------------
# 周公解梦调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/64
# ----------------------------------

def main():
    # 配置您申请的APPKey
    appkey = "2c948f010963c9dbb29cf56e09a2fc56"

    # 1.类型
    #request1(appkey, "GET")

    # 2.解梦查询
    request2(appkey, "GET")

    # 3.根据ID查询解梦信息
    #request3(appkey, "GET")


# 类型
def request1(appkey, m="GET"):
    url = "http://v.juhe.cn/dream/category"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "fid": "",  # 所属分类，默认全部，0:一级分类

    }
    params = parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.parse.urlopen(url, params)

    content = f.read().decode('utf-8')
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return  res["result"]
        else:
            return None
    else:
        return None


# 解梦查询
def request2(appkey,keyword, m="GET"):
    url = " http://v.juhe.cn/dream/query"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "q": keyword,  # 黄金梦境关键字，如：黄金 需要utf8 urlencode
        "cid": "",  # 指定分类，默认全部
        "full": "",  # 是否显示详细信息，1:是 0:否，默认0

    }
    params = parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read().decode('utf-8')
    res = json.loads(content)
    print(res)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return res["result"]
        else:
            return None
    else:
        return None


# 根据ID查询解梦信息
def request3(appkey,ID ,m="GET"):
    url = "http://v.juhe.cn/dream/queryid"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "id": ID,  # 解梦ID

    }
    params = parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read().decode('utf-8')
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return res["result"]
        else:
            return None
    else:
        return None


#if __name__ == '__main__':
#    main()