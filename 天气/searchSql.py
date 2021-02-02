import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

# 取数据用的
def search():
    # 这两句就是访问数据库用的
    conn = sqlite3.connect(path.join(ROOT, 'weather.db'))
    c = conn.cursor()


    cursor = c.execute("SELECT date,yun,temp,detail,img  from weather")
    result = []
    for row in cursor:
        result.append({
            'date': row[0],
            'yun': row[1],
            'temp': row[2],
            'detail': row[3],
            'img': row[4]
        })

    conn.close()
    return result


def searchPassword(username):
    try:
        conn = sqlite3.connect(path.join(ROOT, 'weather.db'))
        c = conn.cursor()

        cursor = c.execute("SELECT password from user where username = '%s'" % username)
        for row in cursor:
            password = row[0]

        conn.close()
        return password
    except:
        return ''

def addUser(username,password):
    try:
        con = sqlite3.connect(path.join(ROOT, 'weather.db'))
        cur = con.cursor()

        sql = 'INSERT INTO user (username,password) VALUES (?,?)'
        data = [username,password]
        cur.execute(sql, data)
        con.commit()

        con.close()
        return True
    except:
        return False






