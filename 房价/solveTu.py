# -*- coding: utf-8 -*-

# 绘制图形用的
import matplotlib.pyplot as plt
import sqlSearch

# 设置图形字体，用于显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 计算出该结果列表中的平均数（总和除总数）
def solveAvg(result):
    # 定义数据字典
    avgResult = {}
    for i in result:
        # 总数
        zongshu = len(result[i])
        # 总和
        Sum = sum(result[i])
        # 平均数求值
        avg = Sum / zongshu
        # 将平均数变整数形式
        avg = int(avg)
        # 把结果存入数据字典
        avgResult[i] = avg
    return avgResult

# 用于展示柱形图中每一行的数据值
def autolabel(rects):
    for rect in rects:
        # 定义长度
        width = rect.get_width()
        # 定义高度
        heigth = rect.get_y()+0.25
        plt.text(width, heigth, width)

# 绘制柱形图函数
def solvePng(avgResult):
    # 初始化图形
    fig, ax = plt.subplots()

    # 定义数组用于记录字典的键和值
    resultKey = []
    resultValue = []

    # 循环之前提取的平均数列表
    for i in avgResult:
        # 将键放进数组
        resultKey.append(i)
        # 将值放进数组
        resultValue.append(avgResult[i])

    # 绘制柱形图
    bath = plt.barh(range(len(resultValue)), resultValue, tick_label=resultKey)
    autolabel(bath)

    # 设置头部和右边的框框可不要
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 设置x轴和y轴标题
    plt.xlabel('价格')
    plt.ylabel('地区')

    # 设置图标题以及保存图的名字
    plt.title('广州房价')
    plt.savefig('static/img/广州房价.png')

# 绘制饼图
def solvePie(jinTwoYear,jinTwoFive,jinFiveTen,jinTenYear):
    labels = ['近两年', '二到五年', '五到十年', '十年以上']
    sizes = [jinTwoYear,jinTwoFive,jinFiveTen,jinTenYear]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    # 设置图标题以及保存图的名字
    plt.title("广州商品房房龄分布")
    plt.savefig('static/img/广州商品房房龄分布.png')


# 最后获取得到结果列表
result = {}
# 近两年房龄的总量列表
jinTwoYear = []
# 二到五年房龄的总量列表
jinTwoFiveYear = []
# 五到十年房龄的总量列表
jinFiveTenYear = []
# 十年以上房龄的总量列表
jinTenYear = []

def chuTu():
    try:
        data = sqlSearch.searchAll()
        for i in data:
            fangDate = i['date']
            if fangDate != '暂无数据':
                fangDate = int(fangDate)
                if fangDate >= 2019:
                    jinTwoYear.append(fangDate)
                elif fangDate >= 2016 and fangDate <= 2018:
                    jinTwoFiveYear.append(fangDate)
                elif fangDate >= 2010 and fangDate <= 2015:
                    jinFiveTenYear.append(fangDate)
                else:
                    jinTenYear.append(fangDate)

            if result.get(i['address']):
                # 则添加进数组
                result[i['address']].append(i['price'])
            else:
                # 没有则新建一个数组，并将结果存入
                result[i['address']] = [i['price']]

        # 将结果交给solveAvg函数处理成平均数列表
        avgResult = solveAvg(result)

        solvePie(len(jinTwoYear), len(jinTwoFiveYear), len(jinFiveTenYear), len(jinTenYear))
        solvePng(avgResult)
        return True
    except Exception as e:
        print(e)
        return False

