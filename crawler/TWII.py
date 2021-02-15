import requests,time, sys, traceback
from bs4 import BeautifulSoup
from crawlerTool import saveMySQL
from crawlerTool import recordLog
from crawlerTool import saveStockCSV

# 擷取執行時間
locTime = time.localtime()

# 設定時間顯示格式
timeStamp = time.strftime('%Y%m%d(%a) %H:%M:%S', locTime)

# 設定日期顯示格式
date = time.strftime('%Y%m%d', locTime)

try:
    log = '{}-執行{}\n'.format(timeStamp, 'TWII')

    # 紀錄log檔
    recordLog(date, log)

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    url1 = 'https://finance.yahoo.com/quote/%5ETWII?p=^TWII&.tsrc=fin-srch'

    ss = requests.session()

    res = ss.get(url = url1, headers = headers)

    # 設定網頁編碼
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')

    # 擷取前一日收盤價
    lastClose = float(str(soup.select('td[class="Ta(end) Fw(600) Lh(14px)"]')[0].text).replace(',',''))


    url = 'https://finance.yahoo.com/quote/%5ETWII/history?p=%5ETWII'

    ss = requests.session()

    res = ss.get(url = url, headers = headers)

    # 設定網頁編碼
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')

    information = soup.select('tr[class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')[0]

    Date_before = information.select('td[class="Py(10px) Ta(start) Pend(10px)"]')[0].text

    Date_change = time.strptime(Date_before, "%b %d, %Y")

    # 交易日期
    MarketDate = time.strftime("%Y/%m/%d", Date_change)

    # 開盤價
    Open = float(information.select('td[class="Py(10px) Pstart(10px)"]')[0].text.replace(',', ''))

    # 計算當日開盤漲跌
    OpenChange = Open - lastClose

    # 最高價
    High = float(information.select('td[class="Py(10px) Pstart(10px)"]')[1].text.replace(',', ''))

    # 最低價
    Low = float(information.select('td[class="Py(10px) Pstart(10px)"]')[2].text.replace(',', ''))

    # 收盤價
    Close = float(information.select('td[class="Py(10px) Pstart(10px)"]')[3].text.replace(',', ''))

    # 擷取當日價格及漲跌幅
    DateChange = soup.select('div[class="D(ib) Mend(20px)"]')[0]

    try:
        # 當日為漲幅
        dateChange = DateChange.select('span[class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)"]')[0].text
    except:
        # 當日為跌幅
        dateChange = DateChange.select('span[class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)"]')[0].text

    dateChange = str(dateChange).replace('%)','').split('(')

    # 每日漲跌
    PriceChange = float(dateChange[0])

    # 每日漲跌幅
    PerChange = float(dateChange[1])

    data = [MarketDate, Open, High, Low, Close,PriceChange,PerChange,OpenChange]

    print('TWII')

    # 執行爬到的資料存入CSV文字檔
    saveStockCSV('TWII', data)

    # 執行將爬到的資料存入MySQL資料庫
    saveMySQL('TWII', data)

# 擷取失敗原因
except Exception as e:

    error_class = e.__class__.__name__  # 取得錯誤類型
    edetail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    elastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    efileName = elastCallStack[0]  # 取得發生的檔案名稱
    elineNum = elastCallStack[1]  # 取得發生的行號
    efuncName = elastCallStack[2]  # 取得發生的函數名稱

    # 失敗原因
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(efileName, elineNum, efuncName, error_class, edetail)

    log = '{}-{}:執行失敗({})\n'.format(timeStamp, 'TWII', errMsg)

    # 紀錄log檔
    recordLog(date, log)

    print(date, '執行失敗({})'.format(errMsg))