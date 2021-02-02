def main(num):
    if num:
        if num == 1:
            return [
                {
                    'num': '1',
                    'href': '?p=1'
                },
                {
                    'num': '下一页',
                    'href': '?p=2'
                },
            ]
        elif num == 30:
            return [
                {
                    'num': '30',
                    'href': '?p=30'
                },
                {
                    'num': '上一页',
                    'href': '?p=29'
                },
            ]
        else:
            return [
                {
                    'num': '上一页',
                    'href': '?p='+str(num-1)
                },
                {
                    'num': str(num),
                    'href': '?p='+str(num)
                },
                {
                    'num': '下一页',
                    'href': '?p='+str(num+1)
                },
            ]
    else:
        return [
            {
                'num': '1',
                'href': '?p=1'
            },
            {
                'num': '下一页',
                'href': '?p=2'
            },
        ]