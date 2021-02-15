#-*-coding:UTF-8 -*-
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
date = str(time.strftime('%Y%m%d', locTime))



try:
    log = '{}-執行{}\n'.format(timeStamp, 'WTXP')

    # 紀錄log檔
    recordLog(date, log)
    
    market_code = 1 #0日盤,1夜盤
    
    url = "https://www.taifex.com.tw/cht/3/futDailyMarketReport"
    
    # 日期市場設定
    myobj = {'queryDate': date, "MarketCode": market_code, "commodity_id": "TX", "queryType": 2}
    
    response = requests.post(url, data=myobj)
    
    soup = BeautifulSoup(response.text, features="html.parser")
    
    table = soup.select("table[class]")[1]
    
    row = table.find_all('tr')[1].find_all('td')[0].text
    
    rowSpilt  = str(row).replace('\t','').replace('\r','').replace(' ','').split('\n')
    
    rowSpilt = list(filter(None,rowSpilt))

    #收盤時間
    closeDate = str(rowSpilt[0]).split('：')[1]

    #交易日期
    marketDate = rowSpilt[2].split('\xa0\xa0')[0]

    # 開盤價
    Open = rowSpilt[20]

    # 最高價
    High = rowSpilt[21]

    # 最低價
    Low = rowSpilt[22]

    # 收盤價
    Close = rowSpilt[23]

    # 每日漲跌
    PriceChange = float(rowSpilt[24].replace('▼','').replace('▲',''))

    # 每日漲跌幅
    PerChange = float(rowSpilt[25].replace('▼','').replace('▲','').replace('%',''))
    
    data = [marketDate, Open, High, Low, Close,PriceChange,PerChange]
    
    print('WTXP')

    # 執行爬到的資料存入CSV文字檔
    saveStockCSV('WTXP', data)

    # 執行將爬到的資料存入MySQL資料庫
    saveMySQL('WTXP', data)

#擷取爬蟲失敗原因
except Exception as e:

    error_class = e.__class__.__name__  # 取得錯誤類型
    edetail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    elastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    efileName = elastCallStack[0]  # 取得發生的檔案名稱
    elineNum = elastCallStack[1]  # 取得發生的行號
    efuncName = elastCallStack[2]  # 取得發生的函數名稱

    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(efileName, elineNum, efuncName, error_class, edetail)

    log = '{}-{}:執行失敗({})\n'.format(timeStamp, 'WTXP', errMsg)

    recordLog(date, log)

    print(date, '執行失敗({})'.format(errMsg))

