import os, pymysql, time, sys, traceback
import pandas as pd
from dotenv import load_dotenv

def recordLog(date,log):
    '''
    每日自動化爬蟲記錄檔
    :param date:檔案執行時間  type=str
    :param log: 爬取的資料紀錄 type=str
    '''

    # 檔案資料夾
    folder = '/home/ec2-user/stockProject/crawlerLog'

    # 如果檔案不存在則建立
    if not os.path.exists(folder):

        os.mkdir(folder)

    path = '{}/{}.txt' .format(folder,date)


    with open(path, 'a', encoding='utf-8') as f:
        f.write(log)



def saveStockCSV(fileName, data):
    '''
    將爬取到的資訊存到CSV檔內
    :param fileName: CSV檔名 type=str
    :param data: 欲存入的資料 type=list
    :return: 處理存檔資訊
    '''


    # 擷取執行時間
    locTime = time.localtime()

    # 設定時間顯示格式
    timeStamp = time.strftime('%Y%m%d(%a) %H:%M:%S', locTime)

    # 設定日期顯示格式
    date = time.strftime('%Y%m%d', locTime)

    try:

        # 如果執行網站為台股現貨
        if fileName == 'TWII':
            strData = '{},{},{},{},{},{},{},{}\n'.format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

        # 如果執行網站為非台股現貨
        else:
            strData = '{},{},{},{},{},{},{}\n'.format(data[0], data[1], data[2], data[3], data[4],data[5], data[6])

        # 讀取csv檔案存成dataframe
        df = pd.read_csv('./{}.csv'.format(fileName))

        Date = []

        # 將日期欄位轉為list
        for i in df['Date']:
            Date.append(i)

        # 如果資料日期不在list裡執行
        if data[0] not in Date:

            with open('./{}.csv'.format(fileName), 'a', encoding='utf-8') as f:

                f.write(strData)

            log = '{}-{}:{} 成功寫入\n'.format(timeStamp,fileName,data[0])

            # 紀錄log檔
            recordLog(date, log)

            return  print(data[0], '成功寫入')

        # 如果資料日期已在list裡執行
        else:
            # 紀錄log檔
            log = '{}-{}:{} 已存在\n'.format(timeStamp,fileName,data[0])

            # 紀錄log檔
            recordLog(date, log)

            return  print(data[0],'資料已存在')

    # 擷取失敗原因
    except Exception as e:

        error_class = e.__class__.__name__  # 取得錯誤類型

        edetail = e.args[0]  # 取得詳細內容

        cl, exc, tb = sys.exc_info()  # 取得Call Stack

        elastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料

        efileName = elastCallStack[0]  # 取得發生的檔案名稱

        elineNum = elastCallStack[1]  # 取得發生的行號

        efuncName = elastCallStack[2]  # 取得發生的函數名稱

        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(efileName, elineNum, efuncName, error_class, edetail)

        log = '{}-{}:{} 執行失敗({})\n'.format(timeStamp, fileName, data[0], errMsg)

        # 紀錄log檔
        recordLog(date, log)

        return print(data[0], '執行失敗({})'.format(errMsg))



def saveMySQL(fileName, data):
    '''
    將爬取到的資料存在關聯式資料庫裡
    :param filename: 表格名稱 type=str
    :param data: 欲存入的資料 type=list
    :return: 處理存檔資訊
    '''

    fileName = str(fileName).replace('\'','')

    load_dotenv()  # 讀取設定檔

    # 擷取執行時間
    locTime = time.localtime()

    # 設定時間顯示格式
    timeStamp = time.strftime('%Y%m%d(%a) %H:%M:%S', locTime)

    # 設定日期顯示格式
    date = time.strftime('%Y%m%d', locTime)

    try:
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

        try:
            try:
                # 如果檔案為TWII 有多一項OpenChange，因此分開
                if fileName == 'TWII':

                    # SQL語法
                    sql = """
                         INSERT INTO {} (Date, Open, High, Low, Close, PriceChange, PerChange, OpenChange)
                        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');
                        """.format(fileName,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

                    # 執行SQL語法
                    cursor.execute(sql)
                    conn.commit()

                    log = '{}-{}:{} 成功存入資料庫\n'.format(timeStamp, fileName, data[0])

                    # 紀錄log檔
                    recordLog(date, log)

                    return print(data[0],'成功存入資料庫')

                # 其餘國家市場爬蟲
                else:
                    # SQL語法
                    sql = """INSERT INTO {} (Date, Open, High, Low, Close, PriceChange, PerChange)
                            VALUES ('{}','{}','{}','{}','{}','{}','{}');""".format(fileName,data[0],data[1],data[2],data[3],data[4],data[5],data[6])

                    # 執行SQL語法
                    cursor.execute(sql)
                    conn.commit()

                    log = '{}-{}:{} 成功存入資料庫\n'.format(timeStamp, fileName, data[0])

                    # 紀錄log檔
                    recordLog(date, log)

                    return print(data[0],'成功存入資料庫')

            # 如果該市場當日資料為NULL(未開盤)
            except pymysql.err.DataError:
                # SQL語法
                sql = """INSERT INTO {} (Date) values ('{}');""".format(fileName, data[0])

                # 執行SQL語法
                cursor.execute(sql)
                conn.commit()

                log = '{}-{}:{} 資料為空值\n'.format(timeStamp, fileName, data[0])

                # 紀錄log檔
                recordLog(date, log)

                return print(data[0], '資料為空值')

        # 如果該市場當日無資料(未開盤)
        except pymysql.err.IntegrityError:

            log = '{}-{}:{} 已在資料庫\n'.format(timeStamp, fileName, data[0])

            # 紀錄log檔
            recordLog(date, log)

            return print(data[0], '已經在資料庫裡了')

        # 關閉游標及連線
        cursor.close()
        conn.close()

    # 擷取失敗原因
    except Exception as e:

        error_class = e.__class__.__name__  # 取得錯誤類型
        edetail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        elastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        efileName = elastCallStack[0]  # 取得發生的檔案名稱
        elineNum = elastCallStack[1]  # 取得發生的行號
        efuncName = elastCallStack[2]  # 取得發生的函數名稱

        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(efileName, elineNum, efuncName, error_class, edetail)

        log = '{}-{}:{} 執行失敗({})\n'.format(timeStamp, fileName, data[0],errMsg)

        # 紀錄log檔
        recordLog(date, log)

        return print(data[0], '執行失敗({})'.format(errMsg))