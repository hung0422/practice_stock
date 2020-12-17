import scrapy
from bs4 import BeautifulSoup
from StockScrapy.items import StockscrapyItem

class stockScrapyCrawler(scrapy.Spider):
    # spider的名子 (於 Terminal 處輸入 scrapy crawl stock_crawler)
    name = 'stock_crawler'
    # 要爬的網址
    start_urls = ['https://finance.yahoo.com/quote/%5ESOX/history?p=%5ESOX',
          'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC',
          'https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC',
          'https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI']
    def parse(self, response, **kwargs):
        res = BeautifulSoup(response.text,'html.parser')
        stockscrapyItem = StockscrapyItem()
        # 名稱
        stockscrapyItem['Name'] = res.select('div[class="D(ib)"]')[0].text.split('^')[1].split(')')[0]
        # 日期
        content = res.select('tr[class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')[1]
        stockscrapyItem['Date'] = content.select('td[class="Py(10px) Ta(start) Pend(10px)"]')[0].text
        # 開盤
        stockscrapyItem['Open'] = float(content.select('td[class="Py(10px) Pstart(10px)"]')[0].text.replace(',',''))
        # 最高
        stockscrapyItem['High'] = float(content.select('td[class="Py(10px) Pstart(10px)"]')[1].text.replace(',', ''))
        # 最低
        stockscrapyItem['Low'] = float(content.select('td[class="Py(10px) Pstart(10px)"]')[2].text.replace(',', ''))
        # 收盤
        stockscrapyItem['Close'] = float(content.select('td[class="Py(10px) Pstart(10px)"]')[3].text.replace(',', ''))
        # 漲跌
        content2 = res.select('div[class="D(ib) Mend(20px)"]')[0]
        stockscrapyItem['PriceChange'] = float(content2.select('span')[1].text.split(' ')[0])
        # 漲跌幅
        stockscrapyItem['PerChange'] = float(content2.select('span')[1].text.split('(')[1].split('%')[0])
        return stockscrapyItem
