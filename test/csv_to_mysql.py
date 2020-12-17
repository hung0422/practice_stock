import pandas as pd
import pymysql

# pymysql設定資料庫連線設定
host = 'localhost'
port = 3306
user = 'test'
passwd = 'test'
db = 'test'
charset = 'utf8mb4'

def CsvToMysql(file):
    # 建立連線
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    # 建立游標
    cursor = conn.cursor()

    # 讀取CSV
    df = pd.read_csv('{}.csv'.format(file))
    # 轉成小數點2位
    df = df.round(2)
    # 刪掉'Adj Close','Volume'
    df2 = df.drop(columns=['Adj Close', 'Volume'])

    # 計算漲跌並加入到dataframe
    # 新增'PriceChange'的list
    PriceChange = [0, ]
    # dataframe轉為list
    df2close = df2.iloc[:, 4]
    listclose = [o for o in df2close]
    # 計算漲跌並放入list
    for i in range(len(listclose)):
        if i == 0:
            pass
        else:
            tmp = listclose[i] - listclose[i - 1]
            PriceChange.append(round(tmp, 2))
    # dataframe中增加'PriceChange'
    df2['PriceChange'] = PriceChange

    # 計算漲跌幅並加入到dataframe
    # 新增'PerChange'的list
    PerChange = [0, ]
    # 計算漲跌幅並放入list
    for i in range(len(listclose)):
        if i == 0:
            pass
        else:
            tmp = PriceChange[i] / listclose[i - 1] * 100
            PerChange.append(round(tmp, 2))
    # dataframe中增加'PerChange'
    df2['PerChange'] = PerChange

    # 第一行(最舊的日期)的漲跌和漲跌幅無法計算因此刪掉
    df3 = df2.iloc[1:, ]

    # dataframe轉為list
    dflist = df3.values.tolist()

    # 執行SQL語法
    for i in dflist:
        sql = """INSERT INTO stock_test (StockName, StockDate, Open, High, Low, Close, PriceChange, PerChange) 
            values ('{}','{}','{}','{}','{}','{}','{}','{}');
            """.format(file, i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        # 將指令放進cursor物件,並執行
        cursor.execute(sql)
    # pymysql預設不會自動commit,所以要加這一行
    conn.commit()
    # 關閉游標及連線
    cursor.close()
    conn.close()

    print('ok')

CsvToMysql('^SOX')
