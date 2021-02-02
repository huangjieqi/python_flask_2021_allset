import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

def search(num):
    conn = sqlite3.connect(path.join(ROOT, '1.db'))
    c = conn.cursor()

    num1 = num*10 - 9
    num = num*10

    cursor = c.execute("SELECT name,address,href,price,date  from main where id between "+str(num1)+" and "+str(num))
    result = []
    for row in cursor:
        result.append({
            'name': row[0],
            'address': row[1],
            'href': row[2],
            'price': row[3],
            'date': row[4]
        })

    conn.close()
    return result

def searchAll():
    conn = sqlite3.connect(path.join(ROOT, '1.db'))
    c = conn.cursor()


    cursor = c.execute("SELECT name,address,href,price,date  from main")
    result = []
    for row in cursor:
        result.append({
            'name': row[0],
            'address': row[1],
            'href': row[2],
            'price': row[3],
            'date': row[4]
        })

    conn.close()
    return result



