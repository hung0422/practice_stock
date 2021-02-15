import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()  # 讀取設定檔

# pymysql設定資料庫連線設定
host = os.getenv("host")
port = int(os.getenv("port"))
user = os.getenv("user")
passwd = os.getenv("passwd")
db = os.getenv("db")
charset = os.getenv("charset")

def CsvToMysql(file):
    '''
    將csv檔案存入mysql
    :param file: 檔案名字 type = str
    :return: 印出OK
    '''
    # 建立連線
    conn = pymysql.connect(host = host, port = port, user = user, passwd = passwd, db = db, charset = charset)
    # 建立游標
    cursor = conn.cursor()

    # 讀取CSV
    df = pd.read_csv('{}.csv'.format(file))

    # 轉成小數點2位
    df = df.round(2)

    # dataframe轉為list
    dflist = df.values.tolist()

    # 執行SQL語法
    for i in dflist:
        try:
            sql = """INSERT INTO {} (Date, Open, High, Low, Close, PriceChange, PerChange) 
                values ('{}','{}','{}','{}','{}','{}','{}');
                """.format(file,i[0], i[1], i[2], i[3], i[4], i[5], i[6])

            # 將指令放進cursor物件,並執行
            cursor.execute(sql)
            print(i)

        # 當Csv當日資料為null時
        except pymysql.err.DataError as DataError:
            sql = """INSERT INTO {} (Date) values ('{}');""".format(file,i[0])
            cursor.execute(sql)
            print(i)

    # pymysql預設不會自動commit,所以要加這一行
    conn.commit()
    # 關閉游標及連線
    cursor.close()
    conn.close()

    return print('ok')

if __name__ == '__main__':
    CsvToMysql('FCHI')