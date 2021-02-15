import os
import datetime
import pymysql
from dotenv import load_dotenv

def settime():
    '''
    查詢今天的日期
    :return: 查詢結果
    '''
    # 現在時間
    locTime = datetime.datetime.now()
    date = locTime.strftime('%Y-%m-%d')
    return date

def sqlopen():
    '''
    設定資料庫連線設定及建立連線與游標
    :return: 連線, 游標
    '''
    load_dotenv()
    # pymysql設定資料庫連線設定
    host = os.getenv("host")
    port = int(os.getenv("port"))
    user = os.getenv("user")
    passwd = os.getenv("passwd")
    db = os.getenv("db")
    charset = os.getenv("charset")

    # 建立連線
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    # 建立游標
    cursor = conn.cursor()
    return conn, cursor

def sqlclose(cursor,conn):
    '''
    關閉資料庫游標及連線
    :param cursor: 資料庫游標
    :param conn: 資料庫連線
    :return: 查詢結果
    '''
    # 關閉游標及連線
    cursor.close()
    conn.close()

def select_perchange(cursor):
    '''
    把要預測資料取出來
    :param cursor: 資料庫游標
    :return: 預測資料
    '''
    data_list = []
    name_list = ['DJI','FCHI','GDAXI','GSPC','HSI','IXIC','KS11','N225','SHI','SOX','TWII','WTXP']
    for name in name_list:
        sql = """SELECT PerChange FROM {} ORDER BY Date DESC LIMIT 1;""".format(name)
        # 將指令放進cursor物件,並執行
        cursor.execute(sql)
        # 將查詢結果取出
        data = cursor.fetchone()
        data_list.append(data)
    return data_list

def predtosql(result,cursor,conn):
    '''
    將預測結果存回資料庫
    :param result: 預測結果
    :param cursor: 資料庫游標
    :param conn: 資料庫連線
    '''
    day = searchday()
    if day == 'Sat':
        date = dayplus2()
    else:
        date = settime()
    # 執行SQL語法
    sql = """INSERT INTO TWII (Date,Prediction)
          VALUES ('{}','{}');""".format(date,result)
    # 將指令放進cursor物件,並執行
    cursor.execute(sql)
    # pymysql預設不會自動commit,所以要加這一行
    conn.commit()

def searchday():
    '''
    判斷今天星期幾
    :return: 縮寫的星期幾
    '''
    # 現在時間
    locTime = datetime.datetime.now()
    day = locTime.strftime('%a')
    return day

def dayplus2():
    '''
    回傳後天的日期
    :return: 查詢結果
    '''
    # 現在時間
    locTime = datetime.datetime.now()
    # 運算日期為 +2天
    delta = datetime.timedelta(days=+2)
    # 後天日期
    acquired = locTime + delta
    date = acquired.strftime('%Y-%m-%d')
    return date