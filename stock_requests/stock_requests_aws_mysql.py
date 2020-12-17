import os
import time
import pymysql
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
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

# 要爬的網址
allurl = ['https://finance.yahoo.com/quote/%5ESOX/history?p=%5ESOX',
          'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC',
          'https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC',
          'https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI']

# 爬蟲設定
ss = requests.session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

for url in allurl:
    res = ss.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 名稱
    Name = soup.select('div[class="D(ib)"]')[0].text.split('^')[1].split(')')[0]
    content = soup.select('tr[class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')[0]
    # 日期
    Date_before = content.select('td[class="Py(10px) Ta(start) Pend(10px)"]')[0].text
    # 轉換時間格式
    Date_change = time.strptime(Date_before, "%b %d, %Y")
    Date = time.strftime("%Y-%m-%d", Date_change)
    # 開盤
    Open = float(content.select('td[class="Py(10px) Pstart(10px)"]')[0].text.replace(',',''))
    # 最高
    High = float(content.select('td[class="Py(10px) Pstart(10px)"]')[1].text.replace(',',''))
    # 最低
    Low = float(content.select('td[class="Py(10px) Pstart(10px)"]')[2].text.replace(',',''))
    # 收盤
    Close = float(content.select('td[class="Py(10px) Pstart(10px)"]')[3].text.replace(',',''))
    # 漲跌
    content2 = soup.select('div[class="D(ib) Mend(20px)"]')[0]
    PriceChange = float(content2.select('span')[1].text.split(' ')[0])
    # 漲跌幅
    PerChange = float(content2.select('span')[1].text.split('(')[1].split('%')[0])

    try:
        # 執行SQL語法
        sql = """
            INSERT INTO {} (Date, Open, High, Low, Close, PriceChange, PerChange)
            VALUES ('{}','{}','{}','{}','{}','{}','{}');
            """.format(Name,Date,Open,High,Low,Close,PriceChange,PerChange)
        # 將指令放進cursor物件,並執行
        cursor.execute(sql)
        # pymysql預設不會自動commit,所以要加這一行
        conn.commit()

        print('Name:', Name)
        print('Date:', Date)
        print('Open:', Open)
        print('High:', High)
        print('Low:', Low)
        print('Close:', Close)
        print('PriceChange:', PriceChange)
        print('PerChange:', PerChange)

    except pymysql.err.IntegrityError:
        print(Date,'的',Name,'已經在資料庫裡了')

# 關閉游標及連線
cursor.close()
conn.close()