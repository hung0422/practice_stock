# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import time
import pymysql

# 轉換時間格式
class Stock_scrapyPipeline:
    def process_item(self, item, spider):
        Date_change = time.strptime(item['Date'], "%b %d, %Y")
        item['Date'] = time.strftime("%Y-%m-%d", Date_change)
        return item

# 將資料存入MySQL
class StockToMysql:
    def open_spider(self, spider):
        # pymysql設定資料庫連線設定
        host = spider.settings.get('HOST')
        port = spider.settings.get('PORT')
        user = spider.settings.get('USER')
        passwd = spider.settings.get('PASSWD')
        db = spider.settings.get("DB")
        charset = spider.settings.get('CHARSET')
        # 建立連線
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        # 建立游標
        self.cursor = self.conn.cursor()
        # pass
    def close_spider(self, spider):
        # 關閉游標及連線
        self.cursor.close()
        self.conn.close()
        # pass
    def process_item(self, item, spider):
        try:
            # 執行SQL語法
            sql = """
                INSERT INTO stock_scrapy (StockName, StockDate, Open, High, Low, Close, PriceChange, PerChange)
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');
                """.format(item['Name'], item['Date'], item['Open'], item['High'], item['Low'], item['Close'],item['PriceChange'],item['PerChange'])
            # 將指令放進cursor物件,並執行
            self.cursor.execute(sql)
            # pymysql預設不會自動commit,所以要加這一行
            self.conn.commit()
            return item

        except pymysql.err.IntegrityError:
            return item['Date'] + ' 的 ' + item['Name'] + ' 已經在資料庫裡了'


