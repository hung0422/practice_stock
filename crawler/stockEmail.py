from crawlerTool import recordLog
from email.mime.text import MIMEText # 專門傳送正文
from email.mime.multipart import MIMEMultipart # 傳送多個部分
from email.mime.application import MIMEApplication # 傳送附件
import smtplib # 傳送郵件
import datetime, os, sys, traceback
from dotenv import load_dotenv

load_dotenv()  # 讀取設定檔
gmailUser = os.getenv('gmailUser') #Email帳號
gmailPasswd = os.getenv('gmailPasswd')#Email密碼
to = ['{}'.format(gmailUser)] #收信者

# 擷取執行時間
locTime = datetime.datetime.now()

# 運算日期為-1天
delta=datetime.timedelta(days=-1)

# 運算昨日日期
yesterday = locTime+delta

# 設定昨日日期顯示格式
yesterday = yesterday.strftime('%Y%m%d')

# 設定時間戳記顯示格式
timeStamp = locTime.strftime('%Y%m%d(%a) %H:%M:%S')

# 設定今日日期顯示格式
date = locTime.strftime('%Y%m%d')

# 檔案位子
file = './crawlerLog/{}.txt'.format(yesterday)  # 附件路徑

try:
    # 如果昨日記錄檔存在
    if os.path.exists(file):
        print('{}-寄送{}國際股市爬蟲單日紀錄報告成功\n'.format(timeStamp, yesterday))

        log = '{}-寄送{}國際股市爬蟲單日紀錄報告成功\n'.format(timeStamp, yesterday)

        # 撰寫記錄檔
        recordLog(date, log)

        send_user = gmailUser   # 發件人
        password = gmailPasswd   # 授權碼/密碼
        receive_users = to   # 收件人，可為list
        subject = '{:s}國際股市爬蟲單日紀錄報告'.format(yesterday)  # 郵件主題
        email_text = """{:s}國際股市爬蟲單日紀錄報告，如附件\n此為系統自動寄送，請勿直接回信，如有問題請直接回報負責人，謝謝合作。""".format(yesterday)   #郵件正文

        msg = MIMEMultipart()
        msg['Subject']=subject    # 主題

        msg['From']=send_user      # 發件人

        for t in receive_users:
            msg['To'] = t           # 收件人

        # 構建正文
        part_text=MIMEText(email_text)
        msg.attach(part_text)             # 把正文加到郵件體裡面去

        # 構建郵件附件
        part_attach1 = MIMEApplication(open(file,'rb').read())   # 開啟附件
        part_attach1.add_header('Content-Disposition','attachment',filename='{}爬蟲程式執行日記報告.txt'.format(yesterday)) #為附件命名
        msg.attach(part_attach1)   # 新增附件

        # Set smtp
        smtp = smtplib.SMTP("smtp.gmail.com:587") # 伺服器地址
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmailUser, gmailPasswd)

        # 寄送郵件
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

        # 刪除已寄出的檔案
        os.remove(file)

    # 如果昨日紀錄檔不存在
    else:
        print('{}-{}國際股市爬蟲單日紀錄報告不存在\n'.format(timeStamp, yesterday))

        log = '{}-寄送{}國際股市爬蟲單日紀錄報告不存在\n'.format(timeStamp, yesterday)

        #撰寫記錄檔
        recordLog(date, log)

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

    log = '{}-{}:執行失敗({})\n'.format(timeStamp, 'stockEmail', errMsg)

    # 撰寫記錄檔
    recordLog(date, log)

    print(date, '執行失敗({})'.format(errMsg))